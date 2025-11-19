from typing import Any

from falcon import Request, Response, status_codes
import pydantic

from classic.error_handling import Error, ErrorsList


def serialize_pydantic_error(
    request: Request, response: Response,
    error: pydantic.ValidationError, params: dict[str, Any],
):
    response.status = status_codes.HTTP_400
    response.media = error.errors(
        include_url=False,
        include_context=False,
        include_input=False,
    )


def serialize_app_error(
    request: Request, response: Response,
    error: Error, params: dict[str, Any],
):
    response.status = status_codes.HTTP_422
    response.media = [{'type': error.code,
                       'msg': error.message,
                       'ctx': error.context}]

def serialize_errors_list(
    request: Request, response: Response,
    error: ErrorsList, params: dict[str, Any],
):
    response.status = status_codes.HTTP_422
    response.media = [
        {'type': e.code,
         'msg': e.message,
         'ctx': e.context}
        for e in error.errors
    ]


def register_error_handlers(app):
    """
    Регистрация обработчиков ошибок в приложении.
    """
    app.add_error_handler(
        pydantic.ValidationError,
        serialize_pydantic_error,
    )
    app.add_error_handler(Error, serialize_app_error)
    app.add_error_handler(ErrorsList, serialize_errors_list)
    return app
