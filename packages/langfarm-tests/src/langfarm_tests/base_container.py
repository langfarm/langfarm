import unittest
from abc import abstractmethod
from typing import final

import sqlalchemy
from sqlalchemy.engine.base import Engine
from testcontainers.core.container import DockerContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer

from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)


class DockerContainerFactory:
    @abstractmethod
    def create_docker_container(self) -> DockerContainer:
        pass

    def after_docker_container_started(self):
        pass

    @abstractmethod
    def docker_container_name(self) -> str:
        pass


class PostgresContainerFactory(DockerContainerFactory):
    def __init__(self):
        self.postgres_container: PostgresContainer | None = None
        self.db_engine: Engine | None = None

    def create_docker_container(self) -> DockerContainer:
        self.postgres_container = PostgresContainer("postgres:latest", driver="psycopg")
        return self.postgres_container

    def after_docker_container_started(self):
        if self.postgres_container:
            self.db_engine = sqlalchemy.create_engine(self.postgres_container.get_connection_url())

    def docker_container_name(self) -> str:
        return "postgres"


class RedisContainerFactory(DockerContainerFactory):
    def __init__(self):
        self.redis_container: RedisContainer | None = None

    def create_docker_container(self) -> DockerContainer:
        self.redis_container = RedisContainer()
        return self.redis_container

    def docker_container_name(self) -> str:
        return "redis"


class KafkaContainerFactory(DockerContainerFactory):
    def __init__(self):
        self.kafka_container: KafkaContainer | None = None

    def create_docker_container(self) -> DockerContainer:
        self.kafka_container = KafkaContainer()
        return self.kafka_container

    def docker_container_name(self) -> str:
        return "kafka"


class DockerComposeTestCase(unittest.TestCase):
    docker_container_dict: dict[str, DockerContainer]

    @classmethod
    @abstractmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        pass

    @classmethod
    def after_docker_compose_started(cls):
        pass

    @classmethod
    @final
    def setUpClass(cls):
        logger.info("create_docker_factory_list for init ...")
        cls.docker_container_dict = {}
        docker_factory_list = cls.create_docker_factory_list()
        for docker_factory in docker_factory_list:
            name = docker_factory.docker_container_name()
            docker_container = docker_factory.create_docker_container()
            cls.docker_container_dict[name] = docker_container
            logger.info(f"{name} DockerContainer starting ...")
            docker_container.start()
            logger.info(f"{name} DockerContainer started!")
            docker_factory.after_docker_container_started()

        cls.after_docker_compose_started()

    @classmethod
    def before_docker_compose_stop(cls):
        pass

    @classmethod
    @final
    def tearDownClass(cls):
        logger.info("stop ...")
        cls.before_docker_compose_stop()
        for name, docker_container in cls.docker_container_dict.items():
            logger.info(f"{name} DockerContainer stopping ...")
            docker_container.stop()
            logger.info(f"{name} DockerContainer stopped!")
