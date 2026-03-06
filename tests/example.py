from dataclasses import dataclass

import pydantic
from falcon import App, Request, Response

from classic.falcon_integration import register_all


# Описывает параметры запроса для GET /api/some_obj
class SomeObjFilter(pydantic.BaseModel):
    number: int


# Описывает структуру ответа
@dataclass
class SomeObj:
    some_attr: int


# Описывает структуру запроса для POST /api/some_obj
class CreateSomeObjRequest(pydantic.BaseModel):
    some_attr: int


class SomeObjResource:

    def on_get(self, request: Request, response: Response):
        # Представим себе, что объекты берутся из БД
        response.media = [
            SomeObj(number)
            for number in range(
                # Объект запроса содержится в контексте под именем query.
                int(request.params['number']),
            )
        ]

    def on_post(self, request: Request, response: Response):
        # Представим себе, что объект был сохранен в БД;)
        response.media = SomeObj(**request.media)


# Композит
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    app = App()
    app.add_route('/api/some_obj', SomeObjResource())

    app = register_all(app)

    # 
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
