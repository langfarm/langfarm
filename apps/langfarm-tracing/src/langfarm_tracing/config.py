from langfarm_app_base.config import AppSettings, PostgresConfig, LangfuseConfig
from langfarm_io.redis import RedisConfig


class Settings(AppSettings, LangfuseConfig, PostgresConfig, RedisConfig):
    API_V1_STR: str = "/api/public"
    PROJECT_NAME: str = "langfarm-tracing"


settings: Settings
"""
使用的时间创建
"""
