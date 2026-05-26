from typing import List
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from browser.application.buckets.read import ReadAllBucketsByConnectionId
from browser.domain.entity.s3_bucket import S3Bucket


def create_read_all_connection_buckets() -> APIRouter:
    router = APIRouter()

    @router.get("/{connection_id:uuid}", status_code=HTTP_200_OK, response_model=List[S3Bucket])
    @inject
    async def read_all_connection(
        interactor: FromDishka[ReadAllBucketsByConnectionId],
        connection_id: UUID
    ):
        return await interactor.execute(connection_id)

    return router