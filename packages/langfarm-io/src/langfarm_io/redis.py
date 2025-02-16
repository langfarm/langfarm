import logging
from typing import Generator

import redis

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RedisConfig(BaseModel):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_BODY_ID_EXPIRE_SECONDS: int = 1800

    def to_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


redis_config: RedisConfig = RedisConfig()
pool: redis.ConnectionPool


def set_redis(config: RedisConfig):
    global redis_config
    redis_config = config
    logger.info("set_redis url=%s", config.to_redis_url())
    global pool
    pool = redis.ConnectionPool(host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT, db=redis_config.REDIS_DB)


def get_redis_client() -> Generator[redis.Redis, None, None]:
    r = redis.Redis(connection_pool=pool)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("redis client=[%s] created", redis_config.to_redis_url())
    try:
        yield r
    finally:
        r.close()
        logger.debug("redis client=[%s] closed", redis_config.to_redis_url())


def with_redis_client(func):
    def execute(key: str, created_at: str, *, expire_seconds: int = redis_config.REDIS_BODY_ID_EXPIRE_SECONDS) -> str:
        for redis_client in get_redis_client():
            return func(key, created_at, expire_seconds=expire_seconds, redis_client=redis_client)

        return created_at

    return execute


@with_redis_client
def read_created_at_or_set(
    key: str,
    created_at: str,
    *,
    expire_seconds: int = redis_config.REDIS_BODY_ID_EXPIRE_SECONDS,
    redis_client: redis.Redis | None = None,
) -> str:
    if not redis_client:
        return created_at
    # https://redis.io/docs/latest/commands/set/
    old_created_at = redis_client.set(key, created_at, ex=expire_seconds, nx=True, get=True)
    if old_created_at:
        return old_created_at.decode("utf-8")  # type: ignore
    else:
        return created_at
