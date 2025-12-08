from celery import Celery

from app.config import settings
from app.helpers.db_helper import db
from app.helpers.rag_helper_ollama import RAGHelperOllama
from app.logger import get_logger
from app.workers.notification.worker import send_discord_notification_task

logger = get_logger("embedding_worker")

# Celery app for embedding worker
embedding_celery = Celery(
    "embedding_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
embedding_celery.conf.task_routes = {
    "generate_embedding_task": {"queue": "embedding_queue"}
}

# Initialize RAG helper
rag_helper = RAGHelperOllama(collection_name=settings.QDRANT_COLL_NAME)


@embedding_celery.task(
    name="generate_embedding_task",
    bind=True,
    autoretry_for=(Exception),
    retry_backoff=True,  # exponential backoff: 1s, 2s, 4s, ...
    retry_backoff_max=60,  # max delay between retries
    retry_jitter=True,  # randomize a bit to avoid thundering herd
    retry_kwargs={"max_retries": 3},  # max retries
    soft_time_limit=40,  # per-task soft limit
    time_limit=50,  # per-task hard limit
)
def generate_embedding_task(task_id: int):
    """
    Generates embedding for task and updates Qdrant.
    Then triggers candidate assignment worker.
    """
    # Fetch task info from DB
    task = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
    if not task:
        logger.error(f"Task {task_id} not found")
        return {"error": f"Task {task_id} not found"}

    task_name = task["title"]
    domain = task.get("domain", "unknown")
    priority = task.get("priority", "medium")
    task_type = task.get("task_type", "other")
    created_by = task.get("created_by", None)

    # Generate embedding and upsert into Qdrant
    metadata = {
        "task_id": task_id,
        "domain": domain,
        "priority": priority,
        "task_type": task_type,
        "created_by": created_by,
    }
    try:
        rag_helper.upsert_document(text=task_name, metadata=metadata)
        logger.info(f"Task {task_id} updated in vector store")
    except Exception as e:
        logger.error(f"Qdrant error: {e}")
        raise e
    
    # send Discord notification
    if created_by:
        user_webhook = db.fetch_one("select * from users where id=%s", (created_by,))
        webhook_url = user_webhook["discord_webhook"]
        if webhook_url:
            embedding_task_embed = {
                "description": f"✅ Your task {task_id} is optimised for semantic search!",
                "color": 0x3498DB,
            }
            send_discord_notification_task.delay(embedding_task_embed, webhook_url)

    return {"task_id": task_id, "status": "embedding_updated"}
