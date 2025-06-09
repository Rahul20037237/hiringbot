from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, ValidationError

class Settings(BaseSettings):
    GROQ_API: SecretStr = Field(..., env="GROQ_API")
    langsmith_tracing: bool = Field(default=False, env="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field(default="https://api.smith.langchain.com", env="LANGSMITH_ENDPOINT")
    langsmith_api_key: SecretStr = Field(default=None, env="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="pg_agi", env="LANGSMITH_PROJECT")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

try:
    settings = Settings()
except ValidationError as e:
    print("❌ Environment configuration is invalid:")
    print(e.json(indent=2))
    raise SystemExit(1)
