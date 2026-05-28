import logging
from dataclasses import dataclass
from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway

logger = logging.getLogger(__name__)

@dataclass
class ReadObjectDownloadUrlResponse:
    url: str

class ReadObjectDownloadUrl:

    def __init__(self, s3_objects_gateway: S3ObjectsGateway):
        self._s3_objects_gateway = s3_objects_gateway

    async def execute(self,
        connection_id: UUID,
        bucket_name: str,
        key: str,
        prefix: str
    ) -> ReadObjectDownloadUrlResponse:
        logger.info("Start generating object download url")

        url = await self._s3_objects_gateway.get_download_url(bucket_name, prefix, key, connection_id)

        result = ReadObjectDownloadUrlResponse(
            url=url
        )

        logger.info("End reading object download url")

        return result