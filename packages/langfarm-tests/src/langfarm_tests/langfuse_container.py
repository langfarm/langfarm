import sqlalchemy

from sqlalchemy.engine.base import Engine
from langfarm_tests.base_container import PostgresContainerFactory, DockerComposeTestCase, DockerContainerFactory
from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)


class LangfuseDBContainerFactory(PostgresContainerFactory):
    def after_docker_container_started(self):
        super().after_docker_container_started()
        # init langfuse db
        # load sql file
        script_file = f"/{__name__}.py"
        logger.info("script file=[%s]", script_file)
        base_dir = __file__[: -len(script_file)]
        sql_file_names = [
            "users.sql",
            "organizations.sql",
            "organization_memberships.sql",
            "projects.sql",
            "api_keys.sql",
            "models.sql",
            "init_data.sql",
        ]
        sql_file_paths = []
        sql_texts: list[str] = []
        for sql_file in sql_file_names:
            sql_file_path = f"{base_dir}/langfarm_tests/init_db/{sql_file}"
            sql_file_paths.append(sql_file_path)
            with open(sql_file_path, "r") as file:
                sql_texts.append(file.read())

        # execute sql for init
        if self.db_engine is None:
            raise Exception("db_engine is None")
        with self.db_engine.begin() as conn:
            for idx in range(len(sql_file_paths)):
                logger.info("import sql in file=[%s]", sql_file_paths[idx])
                result = conn.execute(sqlalchemy.text(sql_texts[idx]))
                logger.info("db exc result:%s", repr(result))


class LangfuseDBContainerTestCase(DockerComposeTestCase):
    langfuse_db_container_factory: LangfuseDBContainerFactory

    @classmethod
    def create_docker_factory_list(cls) -> list[DockerContainerFactory]:
        cls.langfuse_db_container_factory = LangfuseDBContainerFactory()
        return [cls.langfuse_db_container_factory]

    @classmethod
    def get_db_engine(cls) -> Engine:
        if not cls.langfuse_db_container_factory.db_engine:
            logger.error("db_engine is None")
            assert False
        return cls.langfuse_db_container_factory.db_engine
