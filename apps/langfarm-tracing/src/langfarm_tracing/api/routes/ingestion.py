import json
import logging

from fastapi import APIRouter, Depends, Header, HTTPException
from langfarm_io.langfuse import auth
from langfarm_io.langfuse.crud import find_model_by_cache, get_api_key_by_cache
from langfarm_io.langfuse.local_cache import get_cache_info
from langfarm_io.langfuse.schema import ApiKey

from langfarm_tracing.config import settings
from langfarm_tracing.langfuse import events

logger = logging.getLogger(__name__)

router = APIRouter()


async def basic_auth(authorization: str = Header()) -> ApiKey:
    # decode pk, sk
    pk, sk = auth.decode_from_basic_auth(authorization)
    if pk is None:
        raise HTTPException(status_code=401, detail="Invalid credentials. Please configured username.")
    if sk is None:
        raise HTTPException(status_code=401, detail="Invalid credentials. Please configured password.")

    # get api_key
    api_key = get_api_key_by_cache(pk, sk, settings.SALT)
    if api_key is None:
        raise HTTPException(status_code=401, detail="Invalid credentials. Please configured the correct authorization.")
    return api_key


named_cache = {"api_key": get_api_key_by_cache, "model": find_model_by_cache}


@router.get("/cache_info")
async def cache_info(name: str | None = None, clear_cache: bool = False):
    name_list = []
    if name and name in named_cache:
        name_list.append(name)
    else:
        name_list.extend(named_cache.keys())

    named_info = {}
    for _name in name_list:
        named_info[_name] = get_cache_info(named_cache[_name], clear_cache)

    return named_info


@router.get("/find_model")
async def find_model(model_name: str, unit: str | None = None, api_key: ApiKey = Depends(basic_auth)):
    project_id = api_key.project_id
    return find_model_by_cache(model_name, project_id, unit=unit)


handlers = events.create_handlers(kafka_config=settings)


@router.post("")
async def trace_ingestion(data: dict, api_key: ApiKey = Depends(basic_auth)):
    """
    接收 Langfuse 客户端的 trace 上报
    :param data: tracing 内容
    :param api_key: 从 header 的 authorization 取出 pk, sk 在 db 里找到 api_key 的记录。
    :return: {"successes": {"id": "xxx", "status": 201}, "errors": []}
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("/api/public/ingestion => \n%s", json.dumps(data, ensure_ascii=False, indent=4))

    # 取 project_id
    project_id = api_key.project_id
    out = events.events_dispose(data, project_id, handlers)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("out => %s", out)
    return out
