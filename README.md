# Classic Falcon Integration

Предоставляет простую интеграцию веб-фреймворка 
[Falcon](https://falcon.readthedocs.io/en/stable/),
[SpecTree](https://spectree.readthedocs.io/en/latest/index.html),
[orjson](https://github.com/ijl/orjson)
и [classic-error-handling](https://github.com/variasov/classic-error-handling).

## Установка

```bash
pip install classic-falcon-integration
```

## Quickstart

```python
from falcon import App, Request, Response
from spectree import Response as Responses
from pydantic import BaseModel
import waitress

from classic.components import component
from classic.falcon_integration import specification, register_all
from classic import db_tools


class Pet(BaseModel):
    id: int
    name: str
    age: int


class FilterPets(BaseModel):
    name__contains: list[str] | None = None
    age__le: int | None = None
    age__gt: int | None = None
    id: int | None = None


class NewPet(BaseModel):
    name: str
    age: int


@component
class PetsResource:
    db: db_tools.Engine

    @specification(
        query=FilterPets,
        resp=Responses(
            HTTP_200=list[Pet],
        ),
        operation_id='find_pets',
        tags=['pets'],
    )
    def on_get(self, request: Request, response: Response):
        # Валидация по спецификации отключена по умолчанию,
        # потому вызов валидации обязательно добавлять вручную.
        # Валидацию лучше сего проводить через model_validate,
        # так как далее данные все равно будут переданы в виде dict
        FilterPets.model_validate(request.params)

        # Здесь приведен пример работы с БД с classic-db-tools,
        # но здесь может быть что угодно
        with self.db:
            response.media = self.db.queries.filter_pets(
                **request.params
            ).return_as(
                db_tools.ToCls(Pet, id='id'),
                returns=Pet,
            ).many()

    @specification(
        json=NewPet,
        resp=Responses(
            HTTP_200=Pet,
        ),
        tags=['pets'],
    )
    def on_post(self, request: Request, response: Response):
        NewPet.model_validate(request.media)
        with self.db:
            response.media = self.db.queries.save_pet(
                **request.media,
            )


if __name__ == '__main__':
    app = App()
    app.add_route('/api/pets', PetsResource())
    register_all(app)

    waitress.serve(
        app,
        host='127.0.0.1',
        port='8000',
    )
```
