from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from browser.application.buckets.create import CreateBucket

class CreateBucketRequestPydantic(BaseModel):
    name: str

def create_add_bucket_router() -> APIRouter:

    router = APIRouter()

    @router.post("/{connection_id:uuid}", status_code=HTTP_201_CREATED)
    @inject
    async def create_bucket(
        interactor: FromDishka[CreateBucket],
        connection_id: UUID,
        payload: CreateBucketRequestPydantic
    ):
        await interactor.execute(connection_id, payload.name)


    return router