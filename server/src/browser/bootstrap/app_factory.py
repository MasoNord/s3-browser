from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import Provider, AsyncContainer, make_async_container
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from browser.application.exceptions.base import ApplicationError
from browser.bootstrap.ioc.provider_registry import get_providers
from browser.domain.exception.base import DomainError
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.presentation.controllers.exceptions.handler import app_error_handler, infrastructure_error_handler, \
    validation_exception_handler, domain_error_handler
from browser.presentation.controllers.root_router import create_root_router


def create_ioc_container(
    *di_providers: Provider
) -> AsyncContainer:
    return make_async_container(
        *get_providers(),
        *di_providers
    )


def create_web_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )

    app.include_router(create_root_router())
    app.add_exception_handler(ApplicationError, app_error_handler)
    app.add_exception_handler(InfrastructureError, infrastructure_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DomainError, domain_error_handler())

    return app

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = app.state.dishka_container
    try:
        yield
    finally:
        await container.close()
