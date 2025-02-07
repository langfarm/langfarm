from langfarm_tests.base_for_test import get_test_logger, find_env_file

from langfarm_tracing import config

logger = get_test_logger(__name__)

settings = config.settings = config.Settings(
    _env_file=find_env_file(__file__)  # type: ignore
)


def test_tracing_config():
    logger.info("project=%s", settings.PROJECT_NAME)
    assert settings.PROJECT_NAME == "langfarm-tracing"
    assert settings.DOMAIN == "tracing.local.com"
    assert settings.SALT == "mysalt"
    assert settings.POSTGRES_USER == "test"
