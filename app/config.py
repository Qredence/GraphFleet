import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    API_KEY: str = os.getenv("GRAPHRAG_API_KEY", "default_api_key")
    LLM_MODEL: str = os.getenv("GRAPHRAG_LLM_MODEL", "default_llm_model")
    EMBEDDING_MODEL: str = os.getenv("GRAPHRAG_EMBEDDING_MODEL", "text-embedding-3-large")
    API_BASE: str = os.getenv("GRAPHRAG_API_BASE", "default_api_base")
    API_VERSION: str = os.getenv("GRAPHRAG_API_VERSION", "default_api_version")
    INPUT_DIR: str = os.getenv(
        "GRAPHRAG_INPUT_DIR", "graphfleet/output/20240901-044131/artifacts"
    )
    LANCEDB_URI: str = os.getenv(
        "GRAPHRAG_LANCEDB_URI", "graphfleet/output/20240901-044131/artifacts/lancedb"
    )
    COMMUNITY_LEVEL: int = int(os.getenv("GRAPHRAG_COMMUNITY_LEVEL", 2))
    MAX_TOKENS: int = int(os.getenv("GRAPHRAG_MAX_TOKENS", 12000))

    class Config:
        env_prefix = "GRAPHRAG_"

    @property
    def lancedb_uri(self) -> str:
        return f"{self.INPUT_DIR}/lancedb"


settings = Settings()
