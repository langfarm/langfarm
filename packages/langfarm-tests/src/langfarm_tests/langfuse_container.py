import sqlalchemy

from langfarm_tests.base_container import BasePostgresContainerTestCase
from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)


class LangfuseDBContainerTestCase(BasePostgresContainerTestCase):
    @classmethod
    def _set_up_class_other(cls):
        super()._set_up_class_other()
        cls._init_table_and_data()

    @classmethod
    def _init_table_and_data(cls):
        # init langfuse db
        # load sql file
        script_file = f"/{__name__}.py"
        logger.info("script file=[%s]", script_file)
        base_dir = __file__[: -len(script_file)]
        sql_file_names = [
            "users.sql",
            "organizations.sql",
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
        with cls.db_engine.begin() as conn:
            for idx in range(len(sql_file_paths)):
                logger.info("import sql in file=[%s]", sql_file_paths[idx])
                result = conn.execute(sqlalchemy.text(sql_texts[idx]))
                logger.info("db exc result:%s", repr(result))
