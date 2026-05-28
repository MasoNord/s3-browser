from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile, File, Query
from starlette.status import HTTP_204_NO_CONTENT

from browser.application.objects.dto import UploadObject
from browser.application.objects.upload import UploadObjectByConnectionID


def create_s3_file_upload_router() -> APIRouter:

    router = APIRouter()

    @router.post("/{connection_id:uuid}/upload", status_code=HTTP_204_NO_CONTENT)
    @inject
    async def upload_file(
        interactor: FromDishka[UploadObjectByConnectionID],
        connection_id: UUID,
        file: UploadFile = File(),
        bucket_name: str = Query(),
        prefix: str = Query()
    ):

        data = UploadObject(
            file = await file.read(),
            size=file.size,
            content_type=file.content_type,
            bucket_name=bucket_name,
            prefix=prefix,
            filename=file.filename
        )

        await interactor.execute(connection_id, data)

    return router