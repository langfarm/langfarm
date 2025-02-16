from langfarm_app_base.config import AppSettings, LangfuseConfig, PostgresConfig
from langfarm_io.redis import RedisConfig
from pydantic import (
    BaseModel,
    computed_field,
    PostgresDsn,
)
from pydantic_core import MultiHostUrl


class KafkaConfig(BaseModel):
    KAFKA_BOOTSTRAP_SERVERS: str


class Settings(AppSettings, LangfuseConfig, PostgresConfig, RedisConfig, KafkaConfig):  # type: ignore
    API_V1_STR: str = "/api/public"
    PROJECT_NAME: str = "langfarm-tracing"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn(
            MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


settings: Settings
"""
使用的时间创建
"""
