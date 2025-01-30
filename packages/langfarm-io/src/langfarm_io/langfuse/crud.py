from datetime import datetime

from cachetools import cached, TTLCache
from sqlalchemy import select, or_, text, nullslast

from langfarm_io.langfuse import auth
from langfarm_io.langfuse import db_reader
from langfarm_io.langfuse.schema import ApiKey, Model


def select_api_key_by_pk_sk(pk: str, sk: str, salt: str) -> ApiKey | None:
    fast_hashed_secret_key = auth.fast_hashed_secret_key(sk, salt)
    stmt = select(ApiKey).where(ApiKey.fast_hashed_secret_key == fast_hashed_secret_key).where(ApiKey.public_key == pk)
    api_key = db_reader.read_first(stmt, ApiKey)
    return api_key


def find_model(model: str, project_id: str, unit: str | None = None) -> Model | None:
    start_time = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")
    start_time_where = text(f"start_date <= '{start_time}'::timestamp with time zone at time zone 'UTC'")
    stmt = (
        select(Model)
        .where(or_(Model.project_id == project_id, Model.project_id.is_(None)))
        .where(text(":model ~ match_pattern").params({"model": model}))
        .where(or_(start_time_where, Model.start_date.is_(None)))
        .order_by(Model.project_id.asc())
        .order_by(nullslast(Model.start_date.desc()))
        .limit(1)
    )

    if unit:
        stmt = stmt.where(Model.unit == unit)

    model_obj = db_reader.read_first(stmt, Model)
    return model_obj


# 10 分钟 + 256 容量
@cached(cache=TTLCache(maxsize=256, ttl=600), info=True)
def get_api_key_by_cache(pk: str, sk: str, salt: str) -> ApiKey | None:
    api_key = select_api_key_by_pk_sk(pk, sk, salt)
    return api_key


@cached(cache=TTLCache(maxsize=256, ttl=600), info=True)
def find_model_by_cache(model_name: str, project_id: str, unit: str | None = None) -> Model | None:
    return find_model(model_name, project_id, unit=unit)
