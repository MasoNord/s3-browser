from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import Provider, AsyncContainer, make_async_container
from fastapi import FastAPI

from browser.bootstrap.ioc.provider_registry import get_providers
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

    return app

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = app.state.dishka_container
    try:
        yield
    finally:
        await container.close()
