from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from browser.application.s3_settings.update import UpdateS3Setting, UpdateS3SettingRequest
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


class UpdateS3SettingRequestPydantic(BaseModel):
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


def create_update_s3_setting_router() -> APIRouter:

    router = APIRouter()

    @router.put("/{setting_id:uuid}", status_code=HTTP_200_OK, response_model=S3ConnectionSetting)
    @inject
    async def update_setting(
        interactor: FromDishka[UpdateS3Setting],
        setting_id: UUID,
        payload: UpdateS3SettingRequestPydantic
    ):

        update_request = UpdateS3SettingRequest(**payload.model_dump())

        return await interactor.execute(setting_id, update_request)

    return router