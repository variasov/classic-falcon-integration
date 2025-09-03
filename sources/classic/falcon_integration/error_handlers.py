from typing import Any

from falcon import Request, Response
from falcon import status_codes


def register_error_handlers(app):
    try:
        import msgspec

        def serialize_msgspec_error(
            request: Request, response: Response,
            error: msgspec.ValidationError, params: dict[str, Any],
        ):
            response.status = status_codes.HTTP_400
            response.media = str(error)

        app.add_error_handler(
            msgspec.ValidationError,
            serialize_msgspec_error,
        )
    except ImportError:
        pass

    try:
        import pydantic

        def serialize_pydantic_error(
            request: Request, response: Response,
            error: pydantic.ValidationError, params: dict[str, Any],
        ):
            response.status = status_codes.HTTP_400
            response.media = str(error)

        app.add_error_handler(
            pydantic.ValidationError,
            serialize_pydantic_error,
        )

    except ImportError:
        pass

    try:
        from classic.error_handling import Error

        def serialize_app_error(
            request: Request, response: Response,
            error: Error, params: dict[str, Any],
        ):
            response.status = status_codes.HTTP_422
            response.media = [{'type': error.code,
                               'msg': error.message,
                               'ctx': error.context}]

        app.add_error_handler(Error, serialize_app_error)
    except ImportError:
        pass

    try:
        from classic.error_handling import ErrorsList

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

        app.add_error_handler(ErrorsList, serialize_errors_list)
    except ImportError:
        pass
