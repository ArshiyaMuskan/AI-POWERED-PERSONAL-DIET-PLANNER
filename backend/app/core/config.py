from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Personal Diet Planner"
    environment: str = "development"
    secret_key: str = "change-this-in-development"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./diet_planner.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    storage_backend: str = "local"
    local_storage_dir: str = "./storage"
    max_upload_size_mb: int = 5

    ai_provider: str = "local"
    ai_api_url: str | None = None
    ai_api_key: str | None = None
    ai_model: str | None = None

    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_bucket: str = "meal-files"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
