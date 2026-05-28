from fastapi import APIRouter

from browser.presentation.controllers.v1.objects.read import create_read_all_objects_router
from browser.presentation.controllers.v1.objects.upload import create_s3_file_upload_router


def create_objects_router() -> APIRouter:

    router = APIRouter(prefix="/objects", tags=["Objects"])

    router.include_router(create_read_all_objects_router())
    router.include_router(create_s3_file_upload_router())

    return router