from fastapi import APIRouter

from browser.presentation.controllers.v1.objects.read import create_read_all_objects_router


def create_objects_router() -> APIRouter:

    router = APIRouter(prefix="/objects", tags=["Objects"])

    router.include_router(create_read_all_objects_router())

    return router