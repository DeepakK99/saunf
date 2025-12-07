from typing import List
from fastapi import APIRouter, Query
from app.schema.request_entities import TaskRequest
from app.schema.task_response import TaskResponse
from app.workers.main.worker import main_worker_task
from app.workers.embedding.worker import generate_embedding_task
from app.helpers.db_helper import db
from app.logger import get_logger

logger = get_logger("fastapi")
from app.helpers.rag_helper_ollama import RAGHelperOllama

router = APIRouter(prefix="/process", tags=["Processing"])

# Initialize RAG helper (Qdrant collection: tasks_vectors)
rag_helper = RAGHelperOllama(collection_name="tasks_vectors")

@router.post("/process_task")
async def process_task(request: TaskRequest):
    try:
        task_id = request.taskId
        logger.info(f'Received request to process task: {task_id}')
        # Trigger background processing
        main_worker_task.delay(task_id)
        generate_embedding_task.delay(task_id)
        logger.info(f"Task: {task_id} deligatd to main & embedding worker!")
        return {"status": "success", "message": "Task processing started", "taskId": task_id}
    except Exception:
        logger.error(f'Something broke while deligating task: {task_id} to main worker')
        return {"status": "failed", "message": "Task processing failed", "taskId": ""}


@router.get("/search_task", response_model=List[TaskResponse])
async def search_task(
    query: str = Query(..., description="Task name or description to search for"),
    top_k: int = Query(5, description="Number of similar tasks to return")
):
    """
    Search tasks semantically using Qdrant embeddings.
    Returns the top_k most similar tasks to the query.
    """
    # Perform semantic search using RAG helper
    results = rag_helper.search(query=query, limit=top_k)

    # Fetch full task info from DB for matched task_ids
    tasks = []
    for res in results:
        task_id = res["payload"]["task_id"]
        print(task_id)
        task_db = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
        if task_db:
            task_db["score"] = res["score"]  # Add similarity score
            tasks.append(task_db)
    print(tasks)

    return tasks

