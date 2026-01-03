from typing import List

from fastapi import APIRouter, Query

from app.helpers.db_helper import db
from app.helpers.rag_helper_ollama import rag_helper
from app.logger import get_logger
from app.schema.request_entities import TaskRequest
from app.schema.task_response import TaskResponse
from app.workers.embedding.worker import generate_embedding_task
from app.workers.main.worker import main_worker_task

logger = get_logger("fastapi")

router = APIRouter(prefix="/process", tags=["Processing"])

# post endpoint to start processing a task
@router.post("/process_task")
async def process_task(request: TaskRequest):
    try:
        task_id = request.task_id
        logger.info(f"Received request to process task: {task_id}")

        # schedule task in main worker
        main_worker_task.delay(task_id)
        logger.info(f"Task: {task_id} deligated to main worker.")

        # schedule task in embedding worker
        generate_embedding_task.delay(task_id)

        logger.info(f"Task: {task_id} deligatd to embedding worker.")

        return {
            "status": "success",
            "message": "Task processing started",
            "taskId": task_id,
        }
    except Exception as e:
        logger.error(
            f"Something broke while deligating task: {task_id} to main worker.\nErr: {str(e)}"
        )
        return {"status": "failed", "message": "Task processing failed", "taskId": ""}


@router.get("/search_task", response_model=List[TaskResponse])
async def search_task(
    query: str = Query(..., description="Task name or description to search for"),
    top_k: int = Query(5, description="Number of similar tasks to return"),
):
    """
    Search tasks semantically using Qdrant embeddings.
    Returns the top_k most similar tasks to the query.
    """
    try:
        # Perform semantic search using RAG helper
        results = rag_helper.search(query= query, limit= top_k)

        # Fetch full task info from DB for matched task_ids
        tasks = []
        for res in results:
            if res["score"] < 0.5:  # score should be >= 50%
                continue
            task_id = res["payload"]["task_id"]
            task_db = db.fetch_one("SELECT * FROM tasks WHERE id=%s", (task_id,))
            if task_db:
                task_db["score"] = res["score"]  # Add similarity score
                tasks.append(task_db)
        return tasks
    except Exception as e:
        logger.error(f"Error while searching task '{query}'.\nErr: {str(e)}")
        return []
