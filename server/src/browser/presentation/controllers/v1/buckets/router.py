from fastapi import APIRouter

from browser.presentation.controllers.v1.buckets.create import create_add_bucket_router
from browser.presentation.controllers.v1.buckets.read import create_read_all_connection_buckets


def create_bucket_router() -> APIRouter:

    router = APIRouter(prefix="/buckets", tags=["Buckets"])

    router.include_router(create_read_all_connection_buckets())
    router.include_router(create_add_bucket_router())

    return router