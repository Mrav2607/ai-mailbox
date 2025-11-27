from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Blueprint-aligned settings
    app_env: str = Field(default="dev", alias="APP_ENV")
    api_secret: str = Field(default="change_me", alias="API_SECRET")
    database_url: str = Field(default="postgresql+psycopg://user:pass@localhost:5432/ai_mailbox", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    # Back-compat aliases for earlier scaffold usages
    @property
    def APP_NAME(self) -> str:  # pragma: no cover
        return "AI Mailbox API"

    @property
    def ENV(self) -> str:  # pragma: no cover
        return self.app_env

    @property
    def DATABASE_URL(self) -> str:  # pragma: no cover
        return self.database_url

    @property
    def REDIS_URL(self) -> str:  # pragma: no cover
        return self.redis_url

    @property
    def SECRET_KEY(self) -> str:  # pragma: no cover
        return self.api_secret

    class Config:
        env_file = ".env"


settings = Settings()
