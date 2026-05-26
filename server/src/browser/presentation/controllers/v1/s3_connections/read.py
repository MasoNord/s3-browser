from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from browser.application.s3_connections.read import ReadActiveConnections
from browser.domain.entity.s3_connection_config import ConnectionConfig


def create_read_all_active_connections() -> APIRouter:

    router = APIRouter()

    @router.get("/active", status_code=status.HTTP_200_OK, response_model=List[ConnectionConfig])
    @inject
    async def get_active_connections(
        interactor: FromDishka[ReadActiveConnections]
    ):
        return await interactor.execute()

    return router