import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GraphFleet API"
    app_version: str = "1.0.0"
    
    # Azure OpenAI Settings
    azure_openai_api_key: str = os.getenv("GRAPHRAG_API_KEY", "")  # Using GRAPHRAG_API_KEY as per settings.yaml
    azure_openai_api_base: str = os.getenv("AZURE_OPENAI_API_BASE", "https://sweden-azure-oai.openai.azure.com/")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    azure_openai_embedding_deployment: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
    
    # GraphRAG Settings
    graphrag_api_key: str = os.getenv("GRAPHRAG_API_KEY", "")
    graphrag_llm_model: str = os.getenv("GRAPHRAG_LLM_MODEL", "gpt-4o-mini")
    graphrag_embedding_model: str = os.getenv("GRAPHRAG_EMBEDDING_MODEL", "text-embedding-3-large")
    azure_model_embedding_name: str = os.getenv("AZURE_MODEL_EMBEDDING_NAME", "text-embedding-3-large")
    encoding_model: str = "cl100k_base"
    llm_supports_json: bool = True  # Renamed from model_supports_json
    async_mode: str = "threaded"
    
    # Vector Store Settings
    vector_store_type: str = "lancedb"
    vector_store_uri: str = "output/lancedb"
    vector_store_container: str = "default"
    vector_store_overwrite: bool = True
    
    # Input Settings
    input_type: str = "file"
    file_type: str = "text"
    file_encoding: str = "utf-8"
    file_pattern: str = r".*\.txt$"
    
    # Directory Settings
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir: str = os.path.join(base_dir, "input")
    prompts_dir: str = os.path.join(base_dir, "prompts")
    output_dir: str = os.path.join(base_dir, "output")
    pipeline_config: str = os.path.join(base_dir, "pipeline.yml")

    class Config:
        env_file = ".env"
        protected_namespaces = ('settings_',)

@lru_cache()
def get_settings() -> Settings:
    return Settings()
