from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_BROKER: str
    REDIS_BACKEND: str
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    GENERAL_WEBHOOK_URL: str
    OLLAMA_HOST: str
    LLM_MODEL: str
    EMBEDDING_MODEL: str
    LOG_LEVEL: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLL_NAME: str
    

    class Config:
        env_file = ".env"


settings = Settings()
