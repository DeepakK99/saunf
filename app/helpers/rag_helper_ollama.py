from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from typing import List, Dict, Optional
import uuid
from app.helpers.ollama_helper import ollama
from app.config import settings


class RAGHelperOllama:
    """
    RAG helper using Qdrant for vectors and Ollama local model for embeddings.
    Supports metadata filtering in searches.
    """

    def __init__(
        self,
        qdrant_host: str = settings.QDRANT_HOST,
        qdrant_port: int = settings.QDRANT_PORT,
        collection_name: str = settings.QDRANT_COLL_NAME,
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)

        # Ensure collection exists
        if not self.client.collection_exists(self.collection_name):
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance="Cosine"),
            )

    # -------------------------
    # Embedding Generation via Ollama
    # -------------------------
    def generate_embedding(self, text: str) -> List[float]:
        """
        Uses local Ollama embedding model to generate vector.
        """
        embedding = ollama.generate_embedding(text=f"{text}")
        if isinstance(embedding, str):
            embedding = [float(x) for x in embedding.strip("[]").split(",")]
        return embedding

    # -------------------------
    # Upsert/Update Documents
    # -------------------------
    def upsert_document(
        self, text: str, metadata: Optional[Dict] = None
    ) -> str:
        vector = self.generate_embedding(text)
        doc_id = str(uuid.uuid4())
        point = PointStruct(id=doc_id, vector=vector, payload=metadata or {})
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return doc_id

    # -------------------------
    # Search Similar Documents (with optional metadata filter)
    # -------------------------
    def search(
        self,
        query: str,
        limit: int = 5,
        metadata_filter: Optional[Dict[str, str]] = None,
    ) -> List[Dict]:
        """
        Generate embedding for query and search in Qdrant collection.
        Optional `metadata_filter` filters documents by metadata fields.
        """
        query_vector = self.generate_embedding(query)

        q_filter = None
        if metadata_filter:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in metadata_filter.items()
            ]
            q_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=q_filter,
        )

        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]

    # -------------------------
    # Delete Document
    # -------------------------
    def delete_document(self, doc_id: str):
        self.client.delete(
            collection_name=self.collection_name, points_selector={"ids": [doc_id]}
        )

    # -------------------------
    # List all documents
    # -------------------------
    def list_documents(self, limit: int = 100) -> List[Dict]:
        results = self.client.scroll(collection_name=self.collection_name, limit=limit)
        return [{"id": r.id, "payload": r.payload} for r in results]
