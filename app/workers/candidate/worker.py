from celery import Celery
from app.helpers.db_helper import db
from app.config import settings
from app.workers.notification.worker import send_discord_notification_task

# Celery app for candidate assignment
candidate_celery = Celery(
    "candidate_worker",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)
candidate_celery.conf.task_routes = {
    "assign_candidate_task": {"queue": "candidate_queue"}
}


@candidate_celery.task(name="assign_candidate_task")
def assign_candidate_task(task_id: int):
    """
    Assigns the task to the most available user in the same domain.
    """
    # 1️⃣ Fetch task info
    task = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
    if not task:
        raise ValueError(f"Task {task_id} not found")

    domain = task.get("domain")
    hours_needed = task.get("estimated_hours", 1)

    # 2️⃣ Fetch users in the same domain
    users = db.fetch_all("SELECT * FROM users WHERE domain=%s", (domain,))
    if not users:
        raise ValueError(f"No users found for domain {domain}")
    
    # 3️⃣ Compute workload for each user
    user_workload = []
    for user in users:
        user_id = user["id"]
        tasks = db.fetch_all(
            "SELECT estimated_hours FROM tasks WHERE assigned_to=%s AND domain=%s",
            (user_id, domain),
        )
        total_hours = sum(t.get("estimated_hours", 0) for t in tasks)
        user_workload.append((user_id, total_hours))

    # 4️⃣ Select user with least workload
    user_workload.sort(key=lambda x: x[1])
    selected_user_id = user_workload[0][0]

    # 5️⃣ Assign task to user
    db.execute(
        "UPDATE tasks SET assigned_to=%s WHERE id=%s", (selected_user_id, task_id)
    )

    # 6️⃣ Optional: Notify user via Discord
    user = next(u for u in users if u["id"] == selected_user_id)
    message = (
        f"Task auto-assigned to you: {task['title']}\nDomain: {domain}\nHours: {hours_needed}"
    )
    webhook_url = user.get("discord_webhook")  # assume each user has webhook
    if webhook_url:
        send_discord_notification_task.delay(message, webhook_url)

    return {"task_id": task_id, "assigned_to": selected_user_id}
