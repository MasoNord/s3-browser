import logging
from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway
from browser.application.objects.dto import UploadObject

logger = logging.getLogger(__name__)

class UploadObjectByConnectionID:

    def __init__(self, s3_objects_gateway: S3ObjectsGateway):
        self._s3_objects_gateway = s3_objects_gateway

    async def execute(
        self,
        connection_id: UUID,
        data: UploadObject
    ):
        logger.info("Start uploading file: Connection ID: %s", connection_id)
        logger.info("Bucket name: %s", data.bucket_name)
        logger.info("Prefix: %s", data.prefix)


        await self._s3_objects_gateway.upload_object(data, connection_id)

        logger.info("End uploading file")
