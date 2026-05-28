import logging
from uuid import UUID

from browser.application.common.gateway.s3_bucket_gateway import S3BucketGateway

logger = logging.getLogger(__name__)

class CreateBucket:

    def __init__(self, s3_bucket_gateway: S3BucketGateway):
        self._s3_bucket_gateway = s3_bucket_gateway

    async def execute(self, connection_id: UUID, bucket_name: str) -> None:
        logger.info("Start reading all buckets")

        await self._s3_bucket_gateway.create(connection_id, bucket_name)

        return None


