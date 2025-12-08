from time import sleep
from celery import Celery
import requests
from app.config import settings
from datetime import datetime

notification_celery = Celery(
    "notification_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
notification_celery.conf.task_routes = {"send_discord_notification_task": {"queue": "notification_queue"}}


@notification_celery.task(name="send_discord_notification_task",
                            bind=True,
                            autoretry_for=(Exception),
                            retry_backoff=True,             # exponential backoff: 1s, 2s, 4s, ...
                            retry_backoff_max=60,           # max delay between retries
                            retry_jitter=True,              # randomize a bit to avoid thundering herd
                            retry_kwargs={"max_retries": 3},# max retries
                            soft_time_limit=40,             # per-task soft limit
                            time_limit=50,                  # per-task hard limit
                        )
def send_discord_notification_task(message_embed: dict, webhook_url: str):
    if not webhook_url.startswith("http"):
        raise ValueError(f"Invalid webhook URL: {webhook_url}")
    try:
        message_embed["timestamp"] = datetime.now().isoformat()
        response = requests.post(webhook_url, json={"embeds": [message_embed]})
        response.raise_for_status()  # raises an error for bad status codes
        sleep(0.2)
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": str(e)}
    return {"status": response.status_code, "message": message_embed}
