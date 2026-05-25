from fastapi import APIRouter

from browser.presentation.controllers.v1.general.router import create_general_router
from browser.presentation.controllers.v1.s3_connections.router import create_s3_connections_router
from browser.presentation.controllers.v1.s3_settings.router import create_s3_connection_settings_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1")

    router.include_router(create_general_router())
    router.include_router(create_s3_connections_router())
    router.include_router(create_s3_connection_settings_router())

    return router
