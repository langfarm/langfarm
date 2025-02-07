import os
import unittest

import dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

from langfarm_io.langfuse import db_reader
from langfarm_io.langfuse.crud import get_api_key_by_cache
from langfarm_tests.base_for_test import get_test_logger, find_env_file
from langfarm_tests.env_config import LangfuseEnv
from langfarm_tests.langfuse_container import LangfuseDBContainerTestCase
from langfarm_tracing import config

logger = get_test_logger(__name__)

env_paths = find_env_file(__file__)
settings = config.settings = config.Settings(
    _env_file=env_paths  # type: ignore
)


class LangfuseIngestionTestCase(LangfuseDBContainerTestCase):
    app: FastAPI
    client: TestClient

    @classmethod
    def _set_up_class_other(cls):
        super()._set_up_class_other()
        db_reader.engine = cls.db_engine
        my_config = {}
        # load env
        for env_path in env_paths:
            my_config = {**my_config, **dotenv.dotenv_values(env_path)}

        # set config to env
        for k, v in my_config.items():
            if k in os.environ:
                continue
            if v is not None:
                os.environ[k] = v

        from langfarm_tracing.main import app

        cls.client = TestClient(app)
        logger.info("TestClient is started!")

    def test_cache_info(self):
        cache_name = "api_key"
        response = self.client.get(f"{settings.API_V1_STR}/ingestion/cache_info", params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0

        response = self.client.get(f"{settings.API_V1_STR}/ingestion/cache_info")
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0
        assert "model" in response.json()
        assert response.json()["model"]["hits"] == 0
        assert response.json()["model"]["currsize"] == 0

        env = LangfuseEnv()
        api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        response = self.client.get(f"{settings.API_V1_STR}/ingestion/cache_info", params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["misses"] == 1
        assert response.json()[cache_name]["currsize"] == 1

        api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        response = self.client.get(f"{settings.API_V1_STR}/ingestion/cache_info", params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 1
        assert response.json()[cache_name]["misses"] == 1
        assert response.json()[cache_name]["currsize"] == 1

        # 清缓存
        response = self.client.get(
            f"{settings.API_V1_STR}/ingestion/cache_info", params={"name": cache_name, "clear_cache": True}
        )
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0

    def test_find_model(self):
        env = LangfuseEnv()
        b_auth = env.to_basic_auth()
        response = self.client.get(
            f"{settings.API_V1_STR}/ingestion/find_model",
            params={"model_name": "qwen-plus"},
            headers={"authorization": f"Basic {b_auth}"},
        )
        assert response.status_code == 200
        response_data = response.json()
        logger.info("response.json=%s", response_data)
        assert response_data
        assert "id" in response_data
        assert response_data["id"] == "cm3azj5o6000g3rpmxb3iiu8g"

        response = self.client.get(
            f"{settings.API_V1_STR}/ingestion/find_model",
            params={"model_name": "qwen-plus"},
        )
        assert response.status_code == 422

        auths = [" dGhpc19pc19wazp0aGlzX2lzX3Nr", " dGhpc19pc19waw==", ""]
        for b_auth in auths:
            response = self.client.get(
                f"{settings.API_V1_STR}/ingestion/find_model",
                params={"model_name": "qwen-plus"},
                headers={"authorization": f"Basic{b_auth}"},
            )
            assert response.status_code == 401


if __name__ == "__main__":
    unittest.main()
