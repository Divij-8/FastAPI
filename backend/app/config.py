from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", alias="OPENAI_MODEL")
    embeddings_model: str = Field(default="text-embedding-3-small", alias="EMBEDDINGS_MODEL")

    chroma_db_dir: str = Field(default="storage/chroma", alias="CHROMA_DB_DIR")

    cors_allow_origins: List[str] = Field(default_factory=lambda: ["*"], alias="CORS_ALLOW_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: List[str] = Field(default_factory=lambda: ["*"], alias="CORS_ALLOW_METHODS")
    cors_allow_headers: List[str] = Field(default_factory=lambda: ["*"], alias="CORS_ALLOW_HEADERS")

    environment: str = Field(default="development", alias="ENVIRONMENT")
    test_mode: bool = Field(default=False, alias="TEST_MODE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()