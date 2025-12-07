from pydantic import BaseModel

class TaskRequest(BaseModel):
    task_id: int
    