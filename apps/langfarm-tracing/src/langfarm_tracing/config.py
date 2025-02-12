from pydantic import BaseModel
from pydantic import (
    computed_field,
)
from confluent_kafka import Producer
from langfarm_app_base.config import AppSettings, PostgresConfig, LangfuseConfig
from langfarm_io.redis import RedisConfig
from langfarm_tracing import kafka


class KafkaConfig(BaseModel):
    KAFKA_BOOTSTRAP_SERVERS: str


class Settings(AppSettings, LangfuseConfig, PostgresConfig, RedisConfig, KafkaConfig):  # type: ignore
    API_V1_STR: str = "/api/public"
    PROJECT_NAME: str = "langfarm-tracing"

    # 创建 producer
    @computed_field  # type: ignore[prop-decorator]
    @property
    def create_kafka_producer(self) -> Producer:
        return kafka.get_kafka_producer(self)


settings: Settings
"""
使用的时间创建
"""
