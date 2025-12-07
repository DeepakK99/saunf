from pydantic import BaseModel
from typing import Optional

class TaskRAGResponse(BaseModel):
    task_id: int
    name: str
    domain: Optional[str]
    severity: Optional[str]
    task_type: Optional[str]
    assigned_to: Optional[int]
    score: float  # similarity score from RAG search