from langfarm_app_base.config import AppSettings, LangfuseConfig, PostgresConfig
from langfarm_io.redis import RedisConfig
from pydantic import (
    BaseModel,
)


class KafkaConfig(BaseModel):
    KAFKA_BOOTSTRAP_SERVERS: str


class Settings(AppSettings, LangfuseConfig, PostgresConfig, RedisConfig, KafkaConfig):  # type: ignore
    API_V1_STR: str = "/api/public"
    PROJECT_NAME: str = "langfarm-tracing"


settings: Settings
"""
使用的时间创建
"""
