# from app.workers.celery_embedding import generate_embedding_task
import json
import re

from celery import Celery

from app.config import settings
from app.helpers.db_helper import db
from app.helpers.ollama_helper import ollama
from app.logger import get_logger
from app.workers.candidate.worker import assign_candidate_task
from app.workers.notification.worker import send_discord_notification_task

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


@main_celery.task(
    name="main_worker_task",
    bind=True,
    autoretry_for=(Exception),
    retry_backoff=True,  # exponential backoff: 1s, 2s, 4s, ...
    retry_backoff_max=60,  # max delay between retries
    retry_jitter=True,  # randomize a bit to avoid thundering herd
    retry_kwargs={"max_retries": 3},  # max retries
    soft_time_limit=40,  # per-task soft limit
    time_limit=50,  # per-task hard limit
)
def main_worker_task(self, task_id: int):
    """
    Main Celery worker for processing tasks:
    1. Fetch task info from DB
    2. Classify task with Ollama Gemma
    3. Trigger Discord notification
    4. Trigger embedding worker
    """
    logger.info(f"Processing task {task_id} in main worker started!")
    # 1 Fetch task from DB
    task = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
    if not task:
        logger.error(f"Task {task_id} not found!")
        return {"error": f"Task {task_id} not found"}

    task_name = task["title"]
    task_description = task["description"]
    created_by = task["created_by"]

    # 2 Call Ollama Gemma model to classify
    classification = ollama.generate(
        inputs={"task_name": task_name, "task_description": task_description}
    )
    # Parse classification
    try:
        classification = parse_llm_json(classification)
    except json.JSONDecodeError:
        logger.error(f"LLM response for task {task_id} couldn't be parsed! Using default values.")
        classification = {
            "domain": "UNKNOWN",
            "priority": "MEDIUM",
            "task_type": "OTHER",
            "estimated_hours": 0,
        }

    try:
        # 3️ Update task in DB with classification
        db.execute(
            "UPDATE tasks SET domain=%s, priority=%s, task_type=%s, estimated_hours=%s WHERE id=%s",
            (
                classification["domain"],
                classification["priority"],
                classification["task_type"],
                classification["estimated_hours"],
                task_id,
            ),
        )
        logger.info(f"Task {task_id} processed in main worker!")
    except Exception as e:
        logger.error(f"Error updating task: str(e)")
        # let celery retry 
        raise

    # get webhook for the user who created this task
    user_webhook = db.fetch_one(
        "SELECT discord_webhook FROM users WHERE id=%s", (created_by,)
    )
    webhook_url = user_webhook["discord_webhook"]
    # 4️ Trigger Discord notification
    task_status_embed = {
        "title": "📝 Task Processed",
        "description": "Your task has been successfully processed.",
        "color": 0x2ECC71,
        "fields": [
            {"name": "Task Name", "value": task_name, "inline": True},
            {"name": "Domain", "value": classification["domain"], "inline": True},
            {"name": "Priority", "value": classification["priority"], "inline": True},
            {"name": "Task type", "value": classification["task_type"], "inline": True},
            {
                "name": "Estimated Hrs",
                "value": classification["estimated_hours"],
                "inline": True,
            },
        ],
    }
    if webhook_url:
        # send notification as task processed
        send_discord_notification_task.delay(task_status_embed, webhook_url)
        logger.info(f"Notification for task {task_id}(from main worker) scheduled")

    logger.info(f"Task {task_id} deligated to candidate worker")
    # schedule task to find the right candidate and auto assign task
    assign_candidate_task.delay(task_id)

    return {"taskId": task_id, "classification": classification}
