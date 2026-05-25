from fastapi import APIRouter

from browser.presentation.controllers.v1.s3_connections.create import create_create_s3_connection


def create_s3_connections_router() -> APIRouter:

    router = APIRouter(prefix="/s3/connections", tags=["S3 Connections Specific"])

    router.include_router(create_create_s3_connection())

    return router