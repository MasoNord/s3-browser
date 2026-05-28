from typing import List
from uuid import UUID

from browser.application.common.gateway.s3_bucket_gateway import S3BucketGateway
from browser.domain.entity.s3_bucket import S3Bucket
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.infrastructure.s3.s3_connection_manager import AiobotocoreS3ConnectionManager


class AiobotocoreS3BucketGateway(S3BucketGateway):

    def __init__(self, connection_manager: AiobotocoreS3ConnectionManager) -> None:
        self._connection_manager = connection_manager

    async def create(self,  connection_id: UUID, name: str) -> None:
        connection = await self._connection_manager.get_active_connection(connection_id)

        if not connection:
            raise InfrastructureError

        await connection.create_bucket(
            Bucket=name
        )

        return None

    async def read_all(self, connection_id: UUID) -> List[S3Bucket]:
        connection = await self._connection_manager.get_active_connection(connection_id)

        if not connection:
            raise InfrastructureError

        response = await connection.list_buckets()
        await self._connection_manager.ping(connection_id)

        buckets = response["Buckets"]

        return [
            S3Bucket(
                name=b["Name"],
                creation_date=b["CreationDate"]
            ) for b in buckets
        ]


