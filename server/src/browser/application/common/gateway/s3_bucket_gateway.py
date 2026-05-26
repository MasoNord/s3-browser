from abc import abstractmethod
from typing import Protocol, List
from uuid import UUID

from browser.domain.entity.s3_bucket import S3Bucket


class S3BucketGateway(Protocol):

    @abstractmethod
    async def read_all(self, connection_id: UUID) -> List[S3Bucket]:
        raise NotImplementedError