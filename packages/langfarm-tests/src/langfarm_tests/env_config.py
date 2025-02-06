from pydantic import BaseModel


class LangfuseEnv(BaseModel):
    SALT: str = "mysalt"
    LANGFUSE_SECRET_KEY: str = "sk-lf-f69c6951-3462-4997-ba22-1c598e8308aa"
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-a82c2304-c8ee-4b24-aafc-f3d228ca336c"
    PROJECT_ID: str = "cm6g0uptx000613r2ha6hxtkc"
