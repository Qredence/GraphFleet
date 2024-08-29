import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    API_KEY: str = os.getenv("GRAPHRAG_API_KEY")
    LLM_MODEL: str = os.getenv("GRAPHRAG_LLM_MODEL")
    EMBEDDING_MODEL: str = os.getenv("GRAPHRAG_EMBEDDING_MODEL")
    API_BASE: str = os.getenv("GRAPHRAG_API_BASE")
    API_VERSION: str = os.getenv("GRAPHRAG_API_VERSION")
    INPUT_DIR: str = os.getenv("GRAPHRAG_INPUT_DIR")
    LANCEDB_URI: str = os.getenv("GRAPHRAG_LANCEDB_URI")
    COMMUNITY_LEVEL: int = int(os.getenv("GRAPHRAG_COMMUNITY_LEVEL", 2))
    MAX_TOKENS: int = int(os.getenv("GRAPHRAG_MAX_TOKENS", 12000))
    INPUT_DIR: str = "graphfleet/output/20240828-113421/artifacts"
    LANCEDB_URI: str = ""
    COMMUNITY_LEVEL: int = 2

    class Config:
        env_prefix = "GRAPHRAG_"

    @property
    def lancedb_uri(self) -> str:
        return f"{self.INPUT_DIR}/lancedb"


settings = Settings()