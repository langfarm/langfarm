from abc import ABCMeta, abstractmethod

from confluent_kafka import Producer
from langfarm_io import redis as io_redis
from langfarm_io.langfuse import db_reader
from langfarm_tests.base_container import (
    DockerContainerFactory,
    KafkaContainerAware,
    KafkaContainerFactory,
    RedisContainerAware,
    RedisContainerFactory,
)
from langfarm_tests.base_for_test import get_test_logger
from langfarm_tests.langfuse_container import LangfuseDBContainerTestCase

from langfarm_tracing.config import KafkaConfig
from langfarm_tracing.kafka import get_kafka_producer

logger = get_test_logger(__name__)


class TracingKafkaContainerAware(KafkaContainerAware):
    bootstrap_server: str
    producer: Producer

    @classmethod
    def init_kafka_producer(cls):
        cls.bootstrap_server = cls.get_kafka_container().get_bootstrap_server()
        logger.info("kafka bootstrap_server=%s", cls.bootstrap_server)
        cls.producer = get_kafka_producer(KafkaConfig(KAFKA_BOOTSTRAP_SERVERS=cls.bootstrap_server))


class TracingTestContainerTestCase(LangfuseDBContainerTestCase, RedisContainerAware, metaclass=ABCMeta):
    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        factory_list = super().create_docker_factory_list()
        cls.redis_container_factory = RedisContainerFactory()
        factory_list.append(cls.redis_container_factory)
        return factory_list

    @classmethod
    @abstractmethod
    def create_handlers(cls):
        pass

    @classmethod
    def init_handlers(cls):
        pass

    @classmethod
    def init_before_tracing(cls):
        pass

    @classmethod
    def after_docker_compose_started(cls):
        # init db
        db_reader.engine = cls.get_db_engine()

        # init redis
        config = io_redis.RedisConfig(
            REDIS_HOST=cls.get_redis_container().get_container_host_ip(),
            REDIS_PORT=cls.get_redis_container().get_exposed_port(cls.get_redis_container().port),
        )
        io_redis.set_redis(config)

        cls.init_before_tracing()
        cls.create_handlers()
        cls.init_handlers()

    def setUp(self):
        logger.info("")


class TracingWithKafkaTestContainerTestCase(
    TracingTestContainerTestCase, TracingKafkaContainerAware, metaclass=ABCMeta
):
    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        factory_list = super().create_docker_factory_list()
        cls.kafka_container_factory = KafkaContainerFactory()
        factory_list.append(cls.kafka_container_factory)
        return factory_list

    @classmethod
    def init_before_tracing(cls):
        # init kafka
        cls.init_kafka_producer()
