from typing import List
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from browser.application.s3_settings.read import ReadS3SettingsAll, ReadS3ConnectionSettingByID
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


def create_read_all_connection_settings_router() -> APIRouter:

    router = APIRouter()

    @router.get("/read-all", status_code=status.HTTP_200_OK, response_model=List[S3ConnectionSetting])
    @inject
    async def read_all_connection_settings(
        interactor: FromDishka[ReadS3SettingsAll]
    ):
        return await interactor.execute()

    return router

def create_read_connection_setting_by_id_router() -> APIRouter:

    router = APIRouter()

    @router.get("/{settings_id:uuid}", status_code=status.HTTP_200_OK, response_model=S3ConnectionSetting)
    @inject
    async def read_connection_setting_by_id(
        interactor: FromDishka[ReadS3ConnectionSettingByID],
        settings_id: UUID
    ):
        return await interactor.execute(settings_id)

    return router