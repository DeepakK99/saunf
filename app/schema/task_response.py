from pydantic import BaseModel
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    domain: str
    status: str
    task_type: str
    priority: str
    estimated_hours: int
    created_by: int
    assigned_to: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    due_date: datetime
    score: float