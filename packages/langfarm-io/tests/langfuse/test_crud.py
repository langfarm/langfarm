import unittest
from decimal import Decimal

import sqlalchemy
from langfarm_tests.base_for_test import get_test_logger
from langfarm_tests.env_config import LangfuseEnv
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from langfarm_io.langfuse import auth, crud, db_reader
from langfarm_io.langfuse.crud import find_model, find_model_by_cache, get_api_key_by_cache
from langfarm_io.langfuse.local_cache import get_cache_info
from langfarm_io.langfuse.schema import ApiKey
from langfarm_tests.langfuse_container import LangfuseDBContainerTestCase

logger = get_test_logger(__name__)


class UseLangfuseDBTestCase(LangfuseDBContainerTestCase):
    @classmethod
    def after_docker_compose_started(cls):
        db_reader.engine = cls.get_db_engine()

    def test_show_create_api_key_sql(self):
        ct = CreateTable(ApiKey.__table__)  # pyright: ignore
        sql = ct.compile(dialect=postgresql.dialect())
        logger.info("sql=%s", sql)
        assert str(sql).find("WITHOUT TIME ZONE") > 0

    def test_postgresql_connection(self):
        with self.get_db_engine().connect() as conn:
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
        cache_info = get_cache_info(get_api_key_by_cache, clear_cache=True)
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
        cache_info = get_cache_info(find_model_by_cache, clear_cache=True)
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
