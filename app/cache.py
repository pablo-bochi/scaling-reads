import json

import redis

from app.schemas import ProductResponse

REDIS_HOST = "localhost"
REDIS_PORT = 6379
PRODUCT_CACHE_TTL_SECONDS = 60

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def build_product_cache_key(product_id: int) -> str:
    return f"product:{product_id}"


def get_product_cache(product_id: int) -> ProductResponse | None:
    cache_key = build_product_cache_key(product_id)
    cached_value = redis_client.get(cache_key)

    if not cached_value:
        return None

    cached_data = json.loads(cached_value)
    return ProductResponse.model_validate(cached_data)


def set_product_cache(product: ProductResponse) -> None:
    cache_key = build_product_cache_key(product.id)
    redis_client.set(
        cache_key,
        product.model_dump_json(),
        ex=PRODUCT_CACHE_TTL_SECONDS,
    )


def delete_product_cache(product_id: int) -> None:
    cache_key = build_product_cache_key(product_id)
    redis_client.delete(cache_key)
