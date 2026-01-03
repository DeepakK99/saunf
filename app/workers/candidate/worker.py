from celery import Celery
from app.logger import get_logger

from app.config import settings
from app.helpers.db_helper import db
from app.workers.notification.worker import send_discord_notification_task

logger = get_logger("candidate_worker")

# Celery app for candidate assignment
candidate_celery = Celery(
    "candidate_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
candidate_celery.conf.task_routes = {
    "assign_candidate_task": {"queue": "candidate_queue"}
}


@candidate_celery.task(
    name="assign_candidate_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,  # exponential backoff: 1s, 2s, 4s, ...
    retry_backoff_max=60,  # max delay between retries
    retry_jitter=True,  # randomize a bit to avoid thundering herd
    retry_kwargs={"max_retries": 3},  # max retries
    soft_time_limit=40,  # per-task soft limit
    time_limit=50,  # per-task hard limit
)
def assign_candidate_task(self, task_id: int):
    """
    Assigns the task to the most available user in the same domain.
    """
    # Fetch task info
    task = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
    if not task:
        logger.error(f"Task {task_id} not found")
        return {"error": f"Task {task_id} not found"}

    task_name = task.get("title")
    task_type = task.get("task_type")
    priority = task.get("priority")
    domain = task.get("domain")
    created_by = task.get("created_by")
    hours_needed = task.get("estimated_hours", 1)

    # Fetch users in the same domain
    users = db.fetch_all("SELECT * FROM users WHERE domain=%s", (domain,))
    if not users:
        logger.warning(f"No users found for domain {domain}")
        return {"error": f"No users found for domain {domain}"}

    # Compute workload for each user
    min_user_workload = "x", float("inf")
    for user in users:
        user_id = user["id"]
        tasks = db.fetch_all(
            "SELECT estimated_hours FROM tasks WHERE assigned_to=%s AND domain=%s",
            (user_id, domain),
        )
        total_hours = sum(t.get("estimated_hours", 0) for t in tasks)

        if total_hours < min_user_workload[1]:
            min_user_workload = (user_id, total_hours)
        elif total_hours == min_user_workload[1] and str(user_id) == str(created_by): # assign to the task created person if possible
            min_user_workload = (user_id, total_hours)

    # Select user with least workload
    selected_user_id = min_user_workload[0]

    # 5 Assign task to user
    db.execute(
        "UPDATE tasks SET assigned_to=%s WHERE id=%s", (selected_user_id, task_id)
    )

    # Notify user via Discord
    user = next(u for u in users if u["id"] == selected_user_id)

    task_candidate_embed = {
        "title": "🟢 Task Auto-assigned",
        "description": f"Task **{task_name}** has been assigned to you.",
        "color": 0x1ABC9C,  # teal color for assigned tasks
        "fields": [
            {"name": "Task Name", "value": task_name, "inline": True},
            {"name": "Task Type", "value": task_type, "inline": True},
            {"name": "Priority", "value": priority, "inline": True},
            {"name": "Domain", "value": domain, "inline": True},
            {"name": "Estimation", "value": hours_needed, "inline": True},
        ],
    }
    webhook_url = user.get("discord_webhook")
    if webhook_url:
        send_discord_notification_task.delay(task_candidate_embed, webhook_url)

    return {"task_id": task_id, "assigned_to": selected_user_id}
