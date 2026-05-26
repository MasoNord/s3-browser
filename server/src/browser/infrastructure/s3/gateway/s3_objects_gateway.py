from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway
from browser.infrastructure.s3.s3_connection_manager import AiobotocoreS3ConnectionManager


class AiobotocoreS3ObjectsGateway(S3ObjectsGateway):

    def __init__(self, connection_manager: AiobotocoreS3ConnectionManager):
        self._connection_manager = connection_manager


    async def get_objects(self, connection_id: UUID, bucket_name: str, prefix: str | None, delimiter: str = "/",):

        connection = self._connection_manager.get_active_connection(connection_id)

        if not connection:
            raise ConnectionError

        return await connection.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=delimiter,
            Prefix=prefix if prefix else "",
        )
