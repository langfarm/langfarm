import logging

import sqlalchemy
from fastapi import FastAPI
from langfarm_app_base import main

from langfarm_tracing import config

logger = logging.getLogger(__name__)
# uvicorn --env-file PATH 来设置环境变量
settings = config.settings = config.Settings()  # type: ignore


def create_app() -> FastAPI:
    # init db engine
    from langfarm_io.langfuse import db_reader

    db_reader.engine = sqlalchemy.create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

    # init redis client
    from langfarm_io import redis as io_redis

    io_redis.set_redis(settings)

    from langfarm_tracing.api.main import api_router

    return main.create_app(settings, api_router)


app = create_app()
