# langfarm-tests

配置测试的 logging.yaml

使用示例：

```python
from langfarm_tests.base_for_test import get_test_logger

logger = get_test_logger(__name__)

# do something
logger.info("do something")
```

配置文件在 `<root-project-dir>/tests/logging.yaml`
