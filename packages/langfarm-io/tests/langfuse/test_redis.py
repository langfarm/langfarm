import unittest

from langfarm_tests.base_container import (
    DockerComposeTestCase,
    DockerContainerFactory,
    RedisContainerAware,
    RedisContainerFactory,
)
from langfarm_tests.base_for_test import get_test_logger

from langfarm_io import redis as io_redis

logger = get_test_logger(__name__)


class RedisContainerTestCase(DockerComposeTestCase, RedisContainerAware):
    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        cls.redis_container_factory = RedisContainerFactory()
        return [cls.redis_container_factory]

    @classmethod
    def after_docker_compose_started(cls):
        config = io_redis.RedisConfig(
            REDIS_HOST=cls.get_redis_container().get_container_host_ip(),
            REDIS_PORT=cls.get_redis_container().get_exposed_port(cls.get_redis_container().port),
        )
        io_redis.set_redis(config)

    def test_read_created_at_or_set(self):
        created_at = "2024-12-04T16:47:01.292087Z"
        assert io_redis.read_created_at_or_set("test_key", created_at) == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:01.292784Z") == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:03.230789Z") == created_at


if __name__ == "__main__":
    unittest.main()
