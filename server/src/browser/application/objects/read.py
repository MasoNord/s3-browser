import logging
from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway

logger = logging.getLogger(__name__)

class ReadAllObjects:

    def __init__(self, s3_objects_gateway: S3ObjectsGateway):
        self._s3_objects_gateway = s3_objects_gateway

    async def execute(self, connection_id: UUID, bucket_name: str, prefix: str | None, delimiter: str = "/"):

        logger.info("Start reading all objects")

        result = await self._s3_objects_gateway.get_objects(connection_id, bucket_name, prefix, delimiter)


        logger.info("Finish reading all objects")

        return result