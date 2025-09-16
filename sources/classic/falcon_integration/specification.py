from functools import wraps

import falcon
from spectree import SpecTree


spectree = SpecTree('falcon')


@wraps(spectree.validate)
def specification(*args, skip_validation: bool = True, **kwargs):
    return spectree.validate(
        *args,
        skip_validation=skip_validation,
        **kwargs,
    )


@wraps(spectree.register)
def register_specifications(app: falcon.App):
    """
    Регистрация спецификаций SpecTree.
    Регистрацию обязательно проводить ПОСЛЕ регистрации ресурсов в приложении,
    иначе SpecTree не увидит URL-ы ресурсов.
    """
    spectree.register(app)
    return app
