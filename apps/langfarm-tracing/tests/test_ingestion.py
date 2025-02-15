import os
import unittest

import dotenv
from container_for_test import TracingWithKafkaTestContainerTestCase
from fastapi import FastAPI
from fastapi.testclient import TestClient
from langfarm_io.langfuse.crud import get_api_key_by_cache
from langfarm_tests.base_for_test import find_env_file, get_test_logger, read_file_to_dict
from langfarm_tests.env_config import LangfuseEnv

from langfarm_tracing import config

logger = get_test_logger(__name__)

env_paths = find_env_file(__file__)
settings = config.settings = config.Settings(
    _env_file=env_paths  # type: ignore
)


class TestClientBase:
    app: FastAPI
    client: TestClient

    @classmethod
    def init_env(cls):
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

    @classmethod
    def init_test_client(cls):
        from langfarm_tracing.main import app

        cls.client = TestClient(app)
        logger.info("TestClient is started!")


class LangfuseIngestionTestCase(TracingWithKafkaTestContainerTestCase, TestClientBase):
    env: LangfuseEnv
    http_headers: dict[str, str]
    base_url: str

    @classmethod
    def create_handlers(cls):
        cls.init_env()
        os.environ["KAFKA_BOOTSTRAP_SERVERS"] = cls.bootstrap_server
        cls.init_test_client()

        # api env
        cls.env = LangfuseEnv()
        cls.base_url = f"{settings.API_V1_STR}/ingestion"
        b_auth = cls.env.to_basic_auth()
        cls.http_headers = {"authorization": f"Basic {b_auth}"}

    def test_cache_info(self):
        cache_name = "api_key"
        url = f"{self.base_url}/cache_info"

        response = self.client.get(url, params={"clear_cache": True})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0
        assert "model" in response.json()
        assert response.json()["model"]["hits"] == 0
        assert response.json()["model"]["currsize"] == 0

        response = self.client.get(url, params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0

        env = self.env
        api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        response = self.client.get(url, params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["misses"] == 1
        assert response.json()[cache_name]["currsize"] == 1

        api_key = get_api_key_by_cache(env.LANGFUSE_PUBLIC_KEY, env.LANGFUSE_SECRET_KEY, env.SALT)
        assert api_key
        response = self.client.get(url, params={"name": cache_name})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 1
        assert response.json()[cache_name]["misses"] == 1
        assert response.json()[cache_name]["currsize"] == 1

        # 清缓存
        response = self.client.get(url, params={"name": cache_name, "clear_cache": True})
        assert response.status_code == 200
        logger.info("response.json=%s", response.json())
        assert response.json()[cache_name]["hits"] == 0
        assert response.json()[cache_name]["currsize"] == 0

    def test_find_model(self):
        url = f"{self.base_url}/find_model"
        response = self.client.get(
            url,
            params={"model_name": "qwen-plus"},
            headers=self.http_headers,
        )
        assert response.status_code == 200
        response_data = response.json()
        logger.info("response.json=%s", response_data)
        assert response_data
        assert "id" in response_data
        assert response_data["id"] == "cm3azj5o6000g3rpmxb3iiu8g"

        response = self.client.get(
            url,
            params={"model_name": "qwen-plus"},
        )
        assert response.status_code == 422

        auths = [" dGhpc19pc19wazp0aGlzX2lzX3Nr", " dGhpc19pc19waw==", ""]
        for b_auth in auths:
            response = self.client.get(
                url,
                params={"model_name": "qwen-plus"},
                headers={"authorization": f"Basic{b_auth}"},
            )
            assert response.status_code == 401

    def assert_base_trace_ingestion_response(self, response, success_num: int, error_num: int) -> dict:
        assert response.status_code == 200
        response_data = response.json()
        logger.info("response.json=%s", response_data)
        assert response_data
        assert "successes" in response_data
        assert "errors" in response_data
        assert len(response_data["successes"]) == success_num
        assert len(response_data["errors"]) == error_num

        return response_data

    def test_trace_ingestion(self):
        post_data = read_file_to_dict(__file__, "mock-data/trace-02-part1.json")
        response = self.client.post(self.base_url, headers=self.http_headers, json=post_data)
        response_data = self.assert_base_trace_ingestion_response(response, len(post_data["batch"]), 0)
        for idx, success in enumerate(response_data["successes"]):
            assert "id" in success
            assert "status" in success
            assert success["status"] == 201
            assert success["id"] in post_data["batch"][idx]["id"]

    def test_trace_ingestion_post_blank(self):
        # not id
        response = self.client.post(self.base_url, headers=self.http_headers, json={"batch": []})
        self.assert_base_trace_ingestion_response(response, 0, 0)

    def test_trace_ingestion_event_type_not_found_handler(self):
        response = self.client.post(
            self.base_url,
            headers=self.http_headers,
            json={
                "batch": [
                    {
                        "id": "6b79b322-9723-4c28-b66c-ff2fd3f9da54",
                        "type": "xxx-create",
                    }
                ]
            },
        )
        response_data = self.assert_base_trace_ingestion_response(response, 0, 1)
        assert response_data["errors"][0]["id"] == "6b79b322-9723-4c28-b66c-ff2fd3f9da54"
        assert response_data["errors"][0]["status"] == 501

    def test_trace_ingestion_event_miss_body(self):
        response = self.client.post(
            self.base_url,
            headers=self.http_headers,
            json={
                "batch": [
                    {
                        "id": "6b79b322-9723-4c28-b66c-ff2fd3f9da54",
                        "type": "trace-create",
                    }
                ]
            },
        )
        response_data = self.assert_base_trace_ingestion_response(response, 0, 1)
        assert response_data["errors"][0]["id"] == "6b79b322-9723-4c28-b66c-ff2fd3f9da54"
        assert response_data["errors"][0]["status"] == 400
        assert response_data["errors"][0]["message"] == "event 没有找到 body"

    def test_trace_ingestion_event_miss_timestamp(self):
        response = self.client.post(
            self.base_url,
            headers=self.http_headers,
            json={"batch": [{"id": "6b79b322-9723-4c28-b66c-ff2fd3f9da54", "type": "trace-create", "body": {}}]},
        )
        response_data = self.assert_base_trace_ingestion_response(response, 0, 1)
        assert response_data["errors"][0]["id"] == "6b79b322-9723-4c28-b66c-ff2fd3f9da54"
        assert response_data["errors"][0]["status"] == 400
        assert response_data["errors"][0]["message"] == "event 没有找到 timestamp"

    def test_trace_ingestion_body_miss_id(self):
        response = self.client.post(
            self.base_url,
            headers=self.http_headers,
            json={
                "batch": [
                    {
                        "id": "6b79b322-9723-4c28-b66c-ff2fd3f9da54",
                        "type": "trace-create",
                        "body": {},
                        "timestamp": "2024-12-04T16:47:01.292087Z",
                    }
                ]
            },
        )
        response_data = self.assert_base_trace_ingestion_response(response, 0, 1)
        assert response_data["errors"][0]["id"] == "6b79b322-9723-4c28-b66c-ff2fd3f9da54"
        assert response_data["errors"][0]["status"] == 400
        assert response_data["errors"][0]["message"] == "没有找到 body.id"


if __name__ == "__main__":
    unittest.main()
