from langfarm_app_base.config import AppSettings


class Settings(AppSettings):
    API_V1_STR: str = "/api/public"
    PROJECT_NAME: str = "langfarm-tracing"

    # Langfuse
    SALT: str
    LANGFUSE_CACHE_API_KEY_ENABLED: bool = True
    LANGFUSE_CACHE_API_KEY_TTL_SECONDS: int = 600

    # Postgres
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "test"
    POSTGRES_USER: str = "test"
    POSTGRES_PASSWORD: str = "test"


settings: Settings
"""
使用的时间创建
"""
