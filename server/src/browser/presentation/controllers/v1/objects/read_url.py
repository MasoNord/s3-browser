from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette.status import HTTP_200_OK

from browser.application.objects.read_url import ReadObjectDownloadUrlResponse, ReadObjectDownloadUrl


def create_read_object_url_router() -> APIRouter:

    router = APIRouter()

    @router.post("/{connection_id:uuid}/download-url", status_code=HTTP_200_OK, response_model=ReadObjectDownloadUrlResponse)
    @inject
    async def delete_object(
        interactor: FromDishka[ReadObjectDownloadUrl],
        connection_id: UUID,
        bucket_name: str = Query(),
        key: str = Query(),
        prefix: str = Query()
    ):
        return await interactor.execute(connection_id, bucket_name, key, prefix)

    return router