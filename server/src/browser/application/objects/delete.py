import logging
from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway

logger = logging.getLogger(__name__)


class DeleteObjectByConnectionId:

    def __init__(self, s3_objects_gateway: S3ObjectsGateway):
        self._s3_objects_gateway = s3_objects_gateway

    async def execute(
        self,
        connection_id: UUID,
        bucket_name: str,
        key: str,
        prefix: str
    ):
        logger.info("Start uploading file: Connection ID: %s", connection_id)
        logger.info("Bucket name: %s", bucket_name)
        logger.info("Key: %s", key)


        await self._s3_objects_gateway.delete_object(bucket_name, prefix, key, connection_id)

        logger.info("End uploading file")