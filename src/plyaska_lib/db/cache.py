import pickle
from functools import wraps

from beanie import Document


def redis_cache(
    cache_key_template: str | None = None,
    cache_who: Document | None = None,
    cache_by: str | None = None,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from src.main import main

            r = await main.get_connect_cache()
            if cache_key_template and cache_who and cache_by:
                raise RuntimeError(
                    "Need only 2 arguments. cache_who with cache_by "
                    "or cache_key_template with cache_who "
                    "or cache_key_template with cache_by."
                )

            cache_key = ""
            if cache_who:
                cache_key = cache_who.get_settings().name

            if cache_key_template and cache_who:
                cache_key += cache_key_template.format(*args, **kwargs)
            elif cache_key_template:
                template = cache_key_template.lstrip()

                path = template[1 : cache_key_template.find("}")]
                keys = path.split(".")

                if keys[0] != "":
                    obj = kwargs[keys[0]]
                    for key in keys:
                        obj = getattr(obj, key)
                else:
                    obj = args[0]
                    for key in keys[1:]:
                        obj = getattr(obj, key)

                obj = obj.get_settings().name

                cache_key_template2 = (
                    f"{obj}{cache_key_template[cache_key_template.find('}') + 1 :]}"
                )

                cache_key = cache_key_template2.format(*args[1:], **kwargs)

            if cache_by:
                cache_key += f":{cache_by}"

            if value := await r.get(cache_key):
                return pickle.loads(value)
            value = await func(*args, **kwargs)
            value_bytes = pickle.dumps(value)
            await r.set(cache_key, value_bytes)
            return value

        return wrapper

    return decorator
