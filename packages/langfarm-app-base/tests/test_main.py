import unittest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

from langfarm_app_base import main, config
from langfarm_tests.base_for_test import get_test_logger, find_env_file

logger = get_test_logger(__name__)


settings = config.settings = config.Settings(
    _env_file=find_env_file(__file__)  # type: ignore
)

router = APIRouter()


@router.get("/{name}")
def show_name(name: str) -> dict[str, str]:
    return {"name": name}


api_router = APIRouter()
api_router.include_router(router, prefix="/hello", tags=["tests"])


class BaseMainTestCase(unittest.TestCase):
    app: FastAPI
    client: TestClient

    @classmethod
    def setUpClass(cls):
        app = main.create_app(settings, api_router)
        cls.app = app
        client = TestClient(app)
        cls.client = client
        print()
        logger.info("TestClient is started!")

    def setUp(self):
        print()

    def test_hello_name(self):
        response = self.client.get(f"{settings.API_V1_STR}/hello/world")
        assert response.status_code == 200
        assert response.json() == {"name": "world"}


if __name__ == "__main__":
    unittest.main()
