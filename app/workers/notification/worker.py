from datetime import datetime
from time import sleep

import requests
from requests.exceptions import RequestException, HTTPError
from celery import Celery

from app.config import settings
from app.logger import get_logger

logger = get_logger("notification_celery")

# notification celery app
notification_celery = Celery(
    "notification_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
# use notification queue
notification_celery.conf.task_routes = {
    "send_discord_notification_task": {"queue": "notification_queue"}
}


# send notification task
@notification_celery.task(
    name="send_discord_notification_task",
    bind=True,
    autoretry_for=(RequestException,),  # when Exception is raised
    retry_backoff=True,  # exponential backoff: 1s, 2s, 4s, ...
    retry_backoff_max=60,  # max delay between retries
    retry_jitter=True,  # randomize a bit to avoid thundering herd
    retry_kwargs={"max_retries": 3},  # max retries
    soft_time_limit=40,  # per-task soft limit
    time_limit=50,  # per-task hard limit
)
def send_discord_notification_task(self, message_embed: dict, webhook_url: str):
    # avoid accidental non http url call
    if not webhook_url.startswith("http"):
        logger.warning(f"Invalid webhook URL: {webhook_url}")
        return {"error": "Invalid webhook URL"}
    try:
        message_embed["timestamp"] = datetime.now().isoformat()
        response = requests.post(webhook_url, json={"embeds": [message_embed]})
        response.raise_for_status()  # raises an error for bad status codes
        sleep(0.2)
        return {"status": response.status_code, "message": message_embed}
    except HTTPError as e:
        # 4xx errors should NOT be retried
        if 400 <= e.response.status_code < 500:
            logger.error(f"Discord returned non-retryable HTTP error: {str(e)}")
            return {"status": e.response.status_code, "error": str(e)}

        # 5xx errors -> let autoretry_for pick it up
        logger.warning(f"Retryable HTTP error: {str(e)}")
        raise

    except Exception as e:
        # Let Celery handle retry when it's a RequestException(specified in the decorator)
        logger.exception(f"Unexpected error in Discord notification task: {str(e)}")
        raise
