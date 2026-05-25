from fastapi import APIRouter

from browser.presentation.controllers.v1.s3_settings.read import create_read_all_connection_settings_router


def create_s3_connection_settings_router() -> APIRouter:

    router = APIRouter(prefix="/s3/settings", tags=["S3 Settings"])

    router.include_router(create_read_all_connection_settings_router())

    return router