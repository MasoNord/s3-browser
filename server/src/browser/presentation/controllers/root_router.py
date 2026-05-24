from fastapi import APIRouter

from browser.presentation.controllers.v1.api_v1_router import create_api_v1_router


def create_root_router() -> APIRouter:
    router = APIRouter()

    router.include_router(create_api_v1_router())

    return router