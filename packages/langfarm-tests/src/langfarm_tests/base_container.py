import unittest
from abc import abstractmethod
from typing import final

import sqlalchemy
from sqlalchemy.engine.base import Connection, Engine
from testcontainers.core.container import DockerContainer
from testcontainers.postgres import PostgresContainer

from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)


class BaseContainerTestCase(unittest.TestCase):
    tests_container: DockerContainer

    @classmethod
    @abstractmethod
    def _init_docker_container(cls) -> DockerContainer:
        pass

    @classmethod
    @abstractmethod
    def _set_up_class_other(cls):
        pass

    @classmethod
    @final
    def setUpClass(cls):
        cls.tests_container = cls._init_docker_container()
        cls.tests_container.start()
        cls._set_up_class_other()

    @classmethod
    @abstractmethod
    def _tear_down_class_other(cls):
        pass

    @classmethod
    @final
    def tearDownClass(cls):
        cls._tear_down_class_other()
        if cls.tests_container:
            cls.tests_container.stop()


class BasePostgresContainerTestCase(BaseContainerTestCase):
    postgres_container: PostgresContainer
    db_engine: Engine

    @classmethod
    def _set_up_class_other(cls):
        cls.db_engine = sqlalchemy.create_engine(cls.postgres_container.get_connection_url())

    @classmethod
    def _tear_down_class_other(cls):
        pass

    @classmethod
    def _init_docker_container(cls) -> DockerContainer:
        postgres_container = PostgresContainer("postgres:latest", driver="psycopg")
        cls.postgres_container = postgres_container
        return postgres_container

    def setUp(self):
        self.connection: Connection = self.db_engine.connect()
        logger.info("Connected to postgres [%s]", self.postgres_container.get_connection_url())

    def tearDown(self):
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from postgres [%s]", self.postgres_container.get_connection_url())
