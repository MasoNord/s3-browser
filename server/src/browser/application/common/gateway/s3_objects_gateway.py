from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class S3ObjectsGateway(Protocol):

    @abstractmethod
    async def get_objects(self, connection_id: UUID, bucket_name: str, prefix: str | None, delimiter: str = "/"):
        raise NotImplementedError