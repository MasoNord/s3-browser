from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from browser.application.s3_settings.create import CreateS3Setting, CreateS3SettingRequest


class CreateS3SettingRequestPydantic(BaseModel):
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


def create_add_setting_router() -> APIRouter:

    router = APIRouter()

    @router.post("/", status_code=HTTP_201_CREATED)
    @inject
    async def create_setting(
        interactor: FromDishka[CreateS3Setting],
        payload: CreateS3SettingRequestPydantic
    ):

        create_request = CreateS3SettingRequest(**payload.model_dump())

        await interactor.execute(create_request)

    return router