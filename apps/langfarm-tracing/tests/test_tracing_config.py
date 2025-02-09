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

    # postgres
    assert settings.POSTGRES_SERVER == "localhost"
    assert settings.POSTGRES_PORT == 5432
    assert settings.POSTGRES_DB == "test"
    assert settings.POSTGRES_USER == "test"
    assert settings.POSTGRES_PASSWORD == "test"

    # redis
    assert settings.REDIS_BODY_ID_EXPIRE_SECONDS == 600
