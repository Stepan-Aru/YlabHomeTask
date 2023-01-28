import os

import aioredis
from json import dumps, loads
from fastapi.encoders import jsonable_encoder

REDIS_URL = os.environ.get('REDIS_URL')
redis = aioredis.from_url(url=REDIS_URL, encoding='utf-8', decode_responses=True)

REDIS_CACHE_TIME = 300


async def get_cache(name):
    value = await redis.get(name=name)
    return loads(value) if value else None


async def set_cache(name, value):
    return await redis.set(name=name, value=dumps(jsonable_encoder(value)), ex=REDIS_CACHE_TIME)


async def delete_cache(names):
    return await redis.delete(*names)
