from ollama import Client
from app.config import settings
from logger import get_logger
logger = get_logger("ollama_helper")
prompt = """
    Task: {task_name}
    Description: {task_description}
    Please classify the task and estimate no. of hours needed in JSON format:
    {{
        "domain": "FRONTEND/BACKEND/DEVOPS/DESIGN/TESTING",
        "priority": "LOW/MEDIUM/HIGH",
        "task_type": "BUG/FEATURE/ENHANCEMENT/TESTING",
        "estimated_hours": 1/2/3/....
    }}
    return json output only.
    """

class OllamaClient:
    """
    Helper class for local Ollama LLM inference using the official SDK.
    Supports non-streaming responses.
    """

    def __init__(self, host: str = settings.OLLAMA_HOST, model: str = settings.LLM_MODEL):
        # The SDK lets you specify a local or remote Ollama server
        self.client = Client(host=host, timeout=120)
        self.model = model
        self.embedding_model = settings.EMBEDDING_MODEL

    def generate(self, inputs: dict[str]  , options: dict | None = None) -> str:
        """
        Generate a non-streaming response from an LLM using the Ollama SDK.
        """
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt.format(**inputs),
                options=options or {},
            )

            # response["response"] contains the full model output
            return response.get("response", "")
        except Exception as e:
            logger.error(e.message())
            return ""
    
    def generate_embedding(self, text: str):
        try:
            response = self.client.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            embedding = response.get("embedding")
            if not embedding:
                raise ValueError("No embedding returned from Ollama")
            return embedding
        except Exception as e:
            raise e


# Create a global instance similar to `db = MySQLDB()`
ollama = OllamaClient()
