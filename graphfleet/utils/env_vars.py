from pydantic import BaseSettings


class EnvVars(BaseSettings):
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    GOOGLE_CSE_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
