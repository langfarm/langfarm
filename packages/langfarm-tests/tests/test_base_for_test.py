from langfarm_tests.base_for_test import get_package_base_dir, get_test_logger

logger = get_test_logger(__name__)


def test_find_package_base_dir():
    base_dir = get_package_base_dir(__file__)
    logger.info(f"base_dir=[{base_dir}]")
    assert base_dir.endswith("/packages/langfarm-tests")
