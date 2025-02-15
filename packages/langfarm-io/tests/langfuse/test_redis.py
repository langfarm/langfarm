import unittest

from testcontainers.redis import RedisContainer
from langfarm_tests.base_container import DockerComposeTestCase, DockerContainerFactory, RedisContainerFactory

from langfarm_io import redis as io_redis
from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)


class RedisContainerTestCase(DockerComposeTestCase):
    redis_db_container_factory: RedisContainerFactory

    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        cls.redis_db_container_factory = RedisContainerFactory()
        return [cls.redis_db_container_factory]

    @classmethod
    def get_redis_Container(cls) -> RedisContainer:
        if not cls.redis_db_container_factory.redis_container:
            logger.error("redis_container is None")
            assert False
        return cls.redis_db_container_factory.redis_container

    @classmethod
    def after_docker_compose_started(cls):
        config = io_redis.RedisConfig(
            REDIS_HOST=cls.get_redis_Container().get_container_host_ip(),
            REDIS_PORT=cls.get_redis_Container().get_exposed_port(cls.get_redis_Container().port),
        )
        io_redis.set_redis(config)

    def test_read_created_at_or_set(self):
        created_at = "2024-12-04T16:47:01.292087Z"
        assert io_redis.read_created_at_or_set("test_key", created_at) == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:01.292784Z") == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:03.230789Z") == created_at


if __name__ == "__main__":
    unittest.main()
