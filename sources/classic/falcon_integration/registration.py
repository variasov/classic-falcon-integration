import falcon

from .error_handlers import register_error_handlers
from .specification import register_specifications
from .serialization import register_serializer


def register_all(app: falcon.App):
    """
    Регистрирует весь функционал библиотеки разом:
    - обработчики ошибок
    - спецификации
    - сериализация объектов в ответ.

    Регистрацию обязательно проводить ПОСЛЕ регистрации ресурсов в приложении,
    иначе SpecTree не увидит URL-ы ресурсов.
    """
    register_error_handlers(app)
    register_specifications(app)
    register_serializer(app)
    return app
