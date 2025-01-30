import unittest

from langfarm_io.langfuse import auth
from env_config import LangfuseEnv


class MyTestCase(unittest.TestCase):
    def test_decode_from_basic_auth(self):
        my_pk = "this_is_pk"
        my_sk = "this_is_sk"
        authorization = "Basic dGhpc19pc19wazp0aGlzX2lzX3Nr"
        pk, sk = auth.decode_from_basic_auth(authorization)
        assert pk
        assert pk == my_pk

        assert sk
        assert sk == my_sk

        # is only pk
        authorization = "Basic dGhpc19pc19waw=="
        pk, sk = auth.decode_from_basic_auth(authorization)
        assert pk
        assert pk == my_pk

        assert sk is None

        # is pk, sk is blank
        authorization = "Basic dGhpc19pc19wazo="
        pk, sk = auth.decode_from_basic_auth(authorization)
        assert pk
        assert pk == my_pk

        assert sk == ""

    def test_fast_hashed_secret_key(self):
        langfuse_env = LangfuseEnv()
        # langfuse 系统生成的 fast_hashed_secret_key
        fast_hashed_secret_key = "ba74bf29a00183aa793040fc20dc94930e99826c40b0c85ec746688a62f04c47"
        gen_fast_hashed_key = auth.fast_hashed_secret_key(langfuse_env.LANGFUSE_SECRET_KEY, langfuse_env.SALT)
        assert gen_fast_hashed_key == fast_hashed_secret_key


if __name__ == "__main__":
    unittest.main()
