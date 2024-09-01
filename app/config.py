import os


class Settings:
    def __init__(self):
        self.API_KEY: str = os.environ.get("GRAPHRAG_API_KEY", "")
        self.LLM_MODEL: str = os.environ.get("GRAPHRAG_LLM_MODEL", "")
        self.EMBEDDING_MODEL: str = os.environ.get("GRAPHRAG_EMBEDDING_MODEL", "")
        self.API_BASE: str = os.environ.get("GRAPHRAG_API_BASE", "")
        self.API_VERSION: str = os.environ.get("GRAPHRAG_API_VERSION", "")
        self.INPUT_DIR: str = os.environ.get("GRAPHRAG_INPUT_DIR", "graphfleet/output/20240828-113421/artifacts")
        self.LANCEDB_URI: str = f"{self.INPUT_DIR}/lancedb"
        self.COMMUNITY_LEVEL: int = 2
        self.MAX_TOKENS: int = 12000
        self.API_TYPE: str = os.environ.get("GRAPHRAG_API_TYPE", "")


settings = Settings()
