from celery import Celery
from app.config import settings
from app.helpers.db_helper import db
from app.helpers.ollama_helper import ollama
from app.workers.notification.worker import send_discord_notification_task
from app.workers.candidate.worker import assign_candidate_task
# from app.workers.celery_embedding import generate_embedding_task
import json
import re
from app.logger import get_logger
logger = get_logger("main_worker")

def parse_llm_json(response_text: str):
    # Remove ```json or ``` at the start/end
    cleaned = re.sub(r"^```json\s*", "", response_text)
    cleaned = re.sub(r"```$", "", cleaned)

    # Now parse
    return json.loads(cleaned)


# Celery app for main worker
main_celery = Celery(
    "main_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
main_celery.conf.task_routes = {"main_worker_task": {"queue": "main_queue"}}


@main_celery.task(name="main_worker_task")
def main_worker_task(task_id: int):
    """
    Main Celery worker for processing tasks:
    1. Fetch task info from DB
    2. Classify task with Ollama Gemma
    3. Trigger Discord notification
    4. Trigger embedding worker
    """
    logger.info(f'Processing task {task_id} in main worker started!')
    # 1 Fetch task from DB
    task = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
    if not task:
        raise ValueError(f"Task {task_id} not found")

    task_name = task["title"]
    task_description = task["description"]
    created_by = task["created_by"]

    # 2 Call Ollama Gemma model to classify
    classification = ollama.generate(inputs={'task_name':task_name, 
                                     'task_description':task_description})
    # Parse classification
    try:
        classification = parse_llm_json(classification)
    except json.JSONDecodeError:
        logger.error(f"LLM response for task {task_id} couldn't be parsed!")
        classification = {"domain": "UNKNOWN", "priority": "LOW", "task_type": "OTHER", "estimated_hours": 0}

    # 3️ Update task in DB with classification
    db.execute(
        "UPDATE tasks SET domain=%s, priority=%s, task_type=%s, estimated_hours=%s WHERE id=%s",
        (classification["domain"], classification["priority"], classification["task_type"], classification["estimated_hours"], task_id)
    )
    logger.info(f"Task {task_id} processed in main worker!")

    # get webhook for the user who created this task
    user_webhook = db.fetch_one("SELECT discord_webhook FROM users WHERE id=%s", (created_by,))    
    webhook_url = user_webhook["discord_webhook"]
    # 4️ Trigger Discord notification
    message = f"Your Task is Processed!\nTask processed: {task_name}\nDomain: {classification['domain']}\nPriority: {classification['priority']}\nTask type: {classification['task_type']}\nEstimation: {classification['estimated_hours']}hrs"
    if webhook_url:
        logger.info(f'Notification for task {task_id}(main worker) scheduled')
        send_discord_notification_task.delay(message, webhook_url)

    logger.info(f'Task {task_id} deligated to candidate worker')
    # find candidate and auto assign task
    assign_candidate_task.delay(task_id)

    return {"taskId": task_id, "classification": classification}
