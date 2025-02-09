import unittest

from testcontainers.core.container import DockerContainer
from testcontainers.redis import RedisContainer

from langfarm_io import redis as io_redis
from langfarm_tests.base_container import BaseContainerTestCase


class RedisContainerTestCase(BaseContainerTestCase):
    redis_Container: RedisContainer

    @classmethod
    def _init_docker_container(cls) -> DockerContainer:
        cls.redis_Container = RedisContainer()
        return cls.redis_Container

    @classmethod
    def _set_up_class_other(cls):
        config = io_redis.RedisConfig(
            REDIS_HOST=cls.redis_Container.get_container_host_ip(),
            REDIS_PORT=cls.redis_Container.get_exposed_port(cls.redis_Container.port),
        )
        io_redis.set_redis(config)

    @classmethod
    def _tear_down_class_other(cls):
        pass

    def test_read_created_at_or_set(self):
        created_at = "2024-12-04T16:47:01.292087Z"
        assert io_redis.read_created_at_or_set("test_key", created_at) == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:01.292784Z") == created_at
        assert io_redis.read_created_at_or_set("test_key", "2024-12-04T16:47:03.230789Z") == created_at


if __name__ == "__main__":
    unittest.main()
