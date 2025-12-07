from pydantic import BaseModel

class TaskRequest(BaseModel):
    taskId: int
    