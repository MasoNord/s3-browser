from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette.status import HTTP_204_NO_CONTENT

from browser.application.objects.delete import DeleteObjectByConnectionId


def create_delete_object_router() -> APIRouter:

    router = APIRouter()

    @router.delete("/{connection_id:uuid}/delete", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def delete_object(
        interactor: FromDishka[DeleteObjectByConnectionId],
        connection_id: UUID,
        bucket_name: str = Query(),
        key: str = Query(),
        prefix: str = Query()
    ):

        await interactor.execute(connection_id, bucket_name, key, prefix)

    return router