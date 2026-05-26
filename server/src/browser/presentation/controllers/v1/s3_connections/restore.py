from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_204_NO_CONTENT

from browser.application.s3_connections.restore import RestoreS3Connection


def create_restore_connection_router() -> APIRouter:

    router = APIRouter()

    @router.post("/restore/{connection_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def restore_connectio(
        interactor: FromDishka[RestoreS3Connection],
        connection_id: UUID
    ):
        await interactor.execute(connection_id)

    return router