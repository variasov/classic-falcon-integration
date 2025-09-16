from functools import partial

import orjson
from typing import Any

import falcon.media
import pydantic


def default(self, obj: Any):
    if isinstance(obj, pydantic.BaseModel):
        return obj.model_dump_json()
    raise TypeError


def register_serializer(app: falcon.App):
    """
    Регистрация orjson в качестве дефолтного сериализатора.
    Сериализация также будет упаковывать модели pydantic.
    """
    orjson_handler = falcon.media.JSONHandler(
        dumps=partial(orjson.dumps, default=default),
        loads=orjson.loads,
    )
    app.req_options.media_handlers[falcon.MEDIA_JSON] = orjson_handler
    app.resp_options.media_handlers[falcon.MEDIA_JSON] = orjson_handler
    return app
