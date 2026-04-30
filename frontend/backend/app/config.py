from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./hotpulse.db"
    cors_origins: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176"
    crawl_schedule_hour: int = 8
    crawl_schedule_minute: int = 0

    # LLM provider: "anthropic" or "openai" (OpenAI-compatible, e.g. MiMo)
    api_provider: str = "anthropic"
    api_base_url: str = ""
    api_model: str = "claude-sonnet-4-6"
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()
