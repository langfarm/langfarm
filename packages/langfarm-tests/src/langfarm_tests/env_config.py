import base64

from pydantic import BaseModel


class LangfuseEnv(BaseModel):
    SALT: str = "mysalt"
    LANGFUSE_SECRET_KEY: str = "sk-lf-f69c6951-3462-4997-ba22-1c598e8308aa"
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-a82c2304-c8ee-4b24-aafc-f3d228ca336c"
    PROJECT_ID: str = "cm6g0uptx000613r2ha6hxtkc"

    def to_basic_auth(self) -> str:
        basic_auth = f"{self.LANGFUSE_PUBLIC_KEY}:{self.LANGFUSE_SECRET_KEY}"
        b_auth = basic_auth.encode("utf-8")
        encode_basic_auth = base64.b64encode(b_auth).decode("utf-8")
        return encode_basic_auth
