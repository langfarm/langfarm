import unittest
from decimal import Decimal

import sqlalchemy

from langfarm_io.langfuse import crud
from langfarm_io.langfuse.crud import get_api_key_by_cache, find_model, find_model_by_cache
from langfarm_io.langfuse.local_cache import get_cache_info
from langfarm_tests.base_container import BasePostgresContainerTestCase
from langfarm_tests.base_for_test import get_test_logger

from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from langfarm_io.langfuse import auth, db_reader
from langfarm_io.langfuse.schema import ApiKey
from env_config import LangfuseEnv

logger = get_test_logger(__name__)


class UseLangfuseDBTestCase(BasePostgresContainerTestCase):
    @classmethod
    def _set_up_class_other(cls):
        super()._set_up_class_other()
        db_reader.engine = cls.db_engine
        # init langfuse db
        # load sql file
        base_dir = __file__[: -len(f"/{__name__}.py")]
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
            sql_file_path = f"{base_dir}/init_db/{sql_file}"
            sql_file_paths.append(sql_file_path)
            with open(sql_file_path, "r") as file:
                sql_texts.append(file.read())

        # execute sql for init
        with cls.db_engine.begin() as conn:
            for idx in range(len(sql_file_paths)):
                logger.info("import sql in file=[%s]", sql_file_paths[idx])
                result = conn.execute(sqlalchemy.text(sql_texts[idx]))
                logger.info("db exc result:%s", repr(result))

    def test_show_create_api_key_sql(self):
        ct = CreateTable(ApiKey.__table__)  # pyright: ignore
        sql = ct.compile(dialect=postgresql.dialect())
        logger.info("sql=%s", sql)
        assert str(sql).find("WITHOUT TIME ZONE") > 0

    def test_postgresql_connection(self):
        with self.db_engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("select version()"))
            if result:
                row = result.fetchone()
                if row:
                    logger.info("version=%s", row[0])

    def assert_api_key(self, api_key: ApiKey, env: LangfuseEnv):
        assert env
        assert api_key

        logger.info("id = %s", api_key.id)
        logger.info("pk = %s", api_key.public_key)
        logger.info("created_at = %s", api_key.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        assert api_key.public_key == env.LANGFUSE_PUBLIC_KEY
        assert api_key.fast_hashed_secret_key

        sk = env.LANGFUSE_SECRET_KEY
        salt = env.SALT
        fast_hashed = auth.fast_hashed_secret_key(sk, salt)

        assert api_key.fast_hashed_secret_key == fast_hashed

    def test_select_api_key_by_pk_sk(self):
        env = LangfuseEnv()

        # read first
        stmt = select(ApiKey).where(ApiKey.public_key == env.LANGFUSE_PUBLIC_KEY)

        api_key = db_reader.read_first(stmt, ApiKey)
        assert api_key
        self.assert_api_key(api_key, env)

        # select_api_key_by_pk_sk
        api_key = crud.select_api_key_by_pk_sk(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        self.assert_api_key(api_key, env)

    def test_get_api_key_by_cache(self):
        env = LangfuseEnv()
        cache_info = get_cache_info(get_api_key_by_cache)
        assert cache_info
        assert cache_info.currsize == 0
        assert cache_info.hits == 0
        api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        self.assert_api_key(api_key, env)
        cache_info = get_cache_info(get_api_key_by_cache)
        assert cache_info.currsize == 1
        assert cache_info.hits == 0

        new_api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert new_api_key
        assert new_api_key == api_key
        cache_info = get_cache_info(get_api_key_by_cache)
        assert cache_info.currsize == 1
        assert cache_info.hits == 1

    def test_find_model(self):
        env = LangfuseEnv()
        model_name = "qwen-plus"
        model = find_model(model_name, env.PROJECT_ID)
        assert model
        assert model.model_name == model_name
        assert model.input_price == Decimal("0.0000008")
        assert model.output_price == Decimal("0.000002")

        model_name = "qwen-max"
        model = find_model(model_name, env.PROJECT_ID)
        assert model
        assert model.model_name == model_name
        assert model.input_price == Decimal("0.00002")
        assert model.output_price == Decimal("0.00006")

    def test_find_model_by_cache(self):
        env = LangfuseEnv()
        cache_info = get_cache_info(find_model_by_cache)
        assert cache_info
        assert cache_info.currsize == 0
        assert cache_info.hits == 0

        model_name = "qwen-plus"
        model = find_model_by_cache(model_name, env.PROJECT_ID)
        assert model
        assert model.model_name == model_name
        assert model.input_price == Decimal("0.0000008")
        assert model.output_price == Decimal("0.000002")
        cache_info = get_cache_info(find_model_by_cache)
        assert cache_info.currsize == 1
        assert cache_info.hits == 0

        model = find_model_by_cache(model_name, env.PROJECT_ID)
        assert model
        assert model.model_name == model_name
        assert model.input_price == Decimal("0.0000008")
        assert model.output_price == Decimal("0.000002")
        cache_info = get_cache_info(find_model_by_cache)
        assert cache_info.currsize == 1
        assert cache_info.hits == 1


if __name__ == "__main__":
    unittest.main()
