import json
import logging.config
import os.path

import yaml

root_dir = __file__[: -len("/packages/langfarm-tests/src/langfarm_tests/base_for_test.py")]


def config_log(log_file: str):
    # 读取 yaml 格式的日志配置
    with open(log_file) as f:
        log_config = yaml.full_load(f)
        out_log_file = log_config["handlers"]["file_handler"]["filename"]
        log_dir = f"{root_dir}/logs"
        if not os.path.exists(log_dir):
            print("创建日志目录：", log_dir)
            os.makedirs(log_dir, exist_ok=True)
        log_config["handlers"]["file_handler"]["filename"] = f"{root_dir}/{out_log_file}"
        logging.config.dictConfig(log_config)


logger = logging.getLogger(__name__)


def config_log_for_test():
    # 打印空行
    print()

    log_file = f"{root_dir}/tests/logging.yaml"
    print("配置 log_file = ", log_file)

    config_log(log_file)

    logger.info("配置 log_file = %s", log_file)


config_log_for_test()


def get_test_logger(name: str):
    return logging.getLogger(f"tests.{name}")


def get_package_base_dir(test_file: str) -> str:
    idx = test_file.rfind("/tests/")
    package_base_dir = test_file[:idx] if idx > 0 else test_file
    return package_base_dir


def find_env_file(test_file: str, suffix: str = ".test") -> list[str]:
    """
    找 .env{suffix} 配置文件
    :param test_file: 当前的测试文件名，一般用 __file__
    :param suffix: 默认值为 .test 。为拼接为 .env.test
    :return: 顶层项目的 tests 目录 和当前项目的 tests 目录 中找 .env{suffix} 的文件
    """
    package_base_dir = get_package_base_dir(test_file)
    env_file_list = [f"{root_dir}/tests/.env{suffix}", f"{package_base_dir}/tests/.env{suffix}"]
    return env_file_list


def read_file_to_dict(test_file: str, path_to_file: str) -> dict:
    """
    从 path_to_file 读取 json
    :param test_file: __file__
    :param path_to_file: 相对于 <package_base_dir>/tests/ 的文件
    :return: 返回 dict
    """
    package_base_dir = get_package_base_dir(test_file)
    with open(f"{package_base_dir}/tests/{path_to_file}") as f:
        return json.load(f)


def read_file_to_str(test_file: str, path_to_file: str) -> str:
    """
    从 path_to_file 读取 json
    :param test_file: __file__
    :param path_to_file: 相对于 <package_base_dir>/tests/ 的文件
    :return: 返回 str
    """
    package_base_dir = get_package_base_dir(test_file)
    with open(f"{package_base_dir}/tests/{path_to_file}") as f:
        return f.read()
