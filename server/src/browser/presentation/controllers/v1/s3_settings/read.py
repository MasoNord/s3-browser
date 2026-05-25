from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from browser.application.s3_settings.read import ReadS3SettingsAll
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


def create_read_all_connection_settings_router() -> APIRouter:

    router = APIRouter()

    @router.get("/read-all", status_code=status.HTTP_200_OK, response_model=List[S3ConnectionSetting])
    @inject
    async def get_read_all_connection_settings(
        interactor: FromDishka[ReadS3SettingsAll]
    ):
        return await interactor.execute()

    return router