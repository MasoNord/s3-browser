import logging
from typing import List
from uuid import UUID

from browser.application.common.gateway.s3_bucket_gateway import S3BucketGateway
from browser.domain.entity.s3_bucket import S3Bucket

logger = logging.getLogger(__name__)

class ReadAllBucketsByConnectionId:

    def __init__(self, s3_bucket_gateway: S3BucketGateway):
        self._s3_bucket_gateway = s3_bucket_gateway

    async def execute(self, connection_id: UUID) -> List[S3Bucket]:
        logger.info("Start reading all buckets")

        result = await self._s3_bucket_gateway.read_all(connection_id)

        return result
