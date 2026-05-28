import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status

from fastapi import Request
from starlette.responses import Response, JSONResponse
import json

from browser.application.exceptions.base import ApplicationError
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.presentation.controllers.exceptions.constants import ERROR_MESSAGE, ERROR_CODE, ERROR_HTTP_CODE

logger = logging.getLogger(__name__)

async def app_error_handler(request: Request, e: ApplicationError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }

    logger.error("Application Error: %s", str(e))

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )

async def infrastructure_error_handler(request: Request, e: InfrastructureError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }


    logger.error("Infrastructure Error: %s", str(e))

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )

async def exceptions_handler(request: Request, e: Exception) -> Response:
    content = {
        "description": e,
        "unique_code": ERROR_CODE[type(e)],
    }

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(
        "Validation error | method=%s path=%s content_type=%s errors=%s",
        request.method,
        request.url.path,
        request.headers.get("content-type"),
        exc.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": jsonable_encoder(exc.errors())},
    )