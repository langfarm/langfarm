import logging
from pydantic import BaseModel

from langfarm_io.langfuse.crud import get_api_key_by_cache, find_model_by_cache

logger = logging.getLogger(__name__)

named_caches = {"api_key": get_api_key_by_cache, "model": find_model_by_cache}


class CacheInfo(BaseModel):
    hits: int = 0
    misses: int = 0
    maxsize: int = 0
    currsize: int = 0


def _cache_info_to_obj(_cache_info) -> CacheInfo:
    return CacheInfo(hits=_cache_info[0], misses=_cache_info[1], maxsize=_cache_info[2], currsize=_cache_info[3])


def get_cache_info(_cache_handler, clear_cache: bool = False) -> CacheInfo:
    info = _cache_info_to_obj(_cache_handler.cache_info())
    if clear_cache:
        _cache_handler.cache_clear()
        after_info = _cache_info_to_obj(_cache_handler.cache_info())
        logger.info("clear_cache[%s], before=%s, after=%s", _cache_handler.__name__, info, after_info)
        info = after_info
    return info
