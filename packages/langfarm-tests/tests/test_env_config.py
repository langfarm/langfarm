from langfarm_tests.base_for_test import get_test_logger
from langfarm_tests.env_config import LangfuseEnv

logger = get_test_logger(__name__)

a = "cGstbGYtYTgyYzIzMDQtYzhlZS00YjI0LWFhZmMtZjNkMjI4Y2EzMzZjOnNrLWxmLWY2OWM2OTUxLTM0NjItNDk5Ny1iYTIyLTFjNTk4ZTgzMDhhYQ=="


def test_to_basic_auth_str():
    env = LangfuseEnv()
    encode_basic_auth = env.to_basic_auth()
    logger.info("basic_auth=%s", encode_basic_auth)
    assert encode_basic_auth == a
