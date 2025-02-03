from langfarm_tests.base_for_test import find_env_file, get_test_logger

from langfarm_app_base import config

logger = get_test_logger(__name__)

settings = config.settings = config.Settings(
    _env_file=find_env_file(__file__)  # type: ignore
)


def test_tracing_config():
    logger.info("project=%s", settings.PROJECT_NAME)
    assert settings.PROJECT_NAME == "langfarm-app-base"
    assert settings.DOMAIN == "app-base.local.com"
    urls = ["http://localhost/", "http://localhost:4080/", "https://localhost/", "https://localhost:4080/"]
    assert settings.BACKEND_CORS_ORIGINS
    for idx in range(len(urls)):
        assert urls[idx] == str(settings.BACKEND_CORS_ORIGINS[idx])
