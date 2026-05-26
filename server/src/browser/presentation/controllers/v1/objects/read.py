from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette.status import HTTP_200_OK

from browser.application.objects.read import ReadAllObjects


def create_read_all_objects_router() -> APIRouter:

    router = APIRouter()

    @router.get("/{connection_id:uuid}", status_code=HTTP_200_OK)
    @inject
    async def read_all_objects(
        interactor: FromDishka[ReadAllObjects],
        connection_id: UUID,
        bucket_name: str = Query(),
        delimiter: str = Query("/"),
        prefix: str | None= Query(None),
    ):

        return await interactor.execute(connection_id=connection_id, bucket_name=bucket_name, prefix=prefix, delimiter=delimiter)

    return router