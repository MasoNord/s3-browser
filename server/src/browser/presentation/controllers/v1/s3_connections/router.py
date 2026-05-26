from fastapi import APIRouter

from browser.presentation.controllers.v1.s3_connections.create import create_create_s3_connection
from browser.presentation.controllers.v1.s3_connections.read import create_read_all_active_connections
from browser.presentation.controllers.v1.s3_connections.restore import create_restore_connection_router


def create_s3_connections_router() -> APIRouter:

    router = APIRouter(prefix="/s3/connections", tags=["S3 Connections Specific"])

    router.include_router(create_create_s3_connection())
    router.include_router(create_restore_connection_router())
    router.include_router(create_read_all_active_connections())

    return router