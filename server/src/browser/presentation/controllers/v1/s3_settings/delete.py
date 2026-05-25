from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_204_NO_CONTENT
from browser.application.s3_settings.delete import DeleteS3ConnectionSettingById


def create_delete_s3_connection_setting_by_id() -> APIRouter:

    router = APIRouter()

    @router.delete("/{setting_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def delete_s3_connection_setting_by_id(
        interactor: FromDishka[DeleteS3ConnectionSettingById],
        setting_id: UUID
    ):
        await interactor.execute(setting_id)

    return router