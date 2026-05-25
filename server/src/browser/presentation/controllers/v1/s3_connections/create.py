from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

from browser.application.s3_connections.create import CreateS3Connection, CreateS3ConnectionRequest


class CreateS3ConnectionRequestPydantic(BaseModel):
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


def create_create_s3_connection() -> APIRouter:

    router = APIRouter()

    @router.post("/", status_code=status.HTTP_201_CREATED)
    @inject
    async def create_s3_connection(
        interactor: FromDishka[CreateS3Connection],
        payload: CreateS3ConnectionRequestPydantic
    ):
        create_request = CreateS3ConnectionRequest(**payload.model_dump())

        await interactor.execute(create_request)

    return router