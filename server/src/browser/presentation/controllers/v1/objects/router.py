from fastapi import APIRouter

from browser.presentation.controllers.v1.objects.delete import create_delete_object_router
from browser.presentation.controllers.v1.objects.read import create_read_all_objects_router
from browser.presentation.controllers.v1.objects.read_url import create_read_object_url_router
from browser.presentation.controllers.v1.objects.upload import create_s3_file_upload_router


def create_objects_router() -> APIRouter:

    router = APIRouter(prefix="/objects", tags=["Objects"])

    router.include_router(create_read_all_objects_router())
    router.include_router(create_s3_file_upload_router())
    router.include_router(create_delete_object_router())
    router.include_router(create_read_object_url_router())

    return router