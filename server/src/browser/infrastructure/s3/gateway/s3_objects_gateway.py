import logging
from uuid import UUID

from botocore.exceptions import ClientError

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway
from browser.application.objects.dto import UploadObject
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.infrastructure.s3.s3_connection_manager import AiobotocoreS3ConnectionManager

logger = logging.getLogger(__name__)

class AiobotocoreS3ObjectsGateway(S3ObjectsGateway):

    def __init__(self, connection_manager: AiobotocoreS3ConnectionManager):
        self._connection_manager = connection_manager


    async def get_objects(self, connection_id: UUID, bucket_name: str, prefix: str | None, delimiter: str = "/",):

        connection = await self._connection_manager.get_active_connection(connection_id)

        if not connection:
            raise ConnectionError

        return await connection.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=delimiter,
            Prefix=prefix if prefix else "",
        )

    async def upload_object(self, data: UploadObject, connection_id: UUID):
        logger.info("File uploading started: PREFIX: %s", data.prefix)

        connection = await self._connection_manager.get_active_connection(connection_id)

        if not connection:
            raise ConnectionError

        try:
            prefix = data.prefix or ""

            if prefix and not prefix.endswith("/"):
                prefix += "/"

            object_key = f"{prefix}{data.filename}"

            await connection.put_object(
                Bucket=data.bucket_name,
                Key=object_key,
                Body=data.file,
                ContentType=data.content_type,
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            logger.error("Error uploading object: %s - %s", error_code, error_message)
            raise InfrastructureError

        logger.info("File uploading ended")

        return data.prefix

    async def delete_object(self, bucket_name: str, prefix: str, key: str, connection_id: UUID):
        try:
            connection = await self._connection_manager.get_active_connection(connection_id)
            prefix = prefix or ""

            if prefix and not prefix.endswith("/"):
                prefix += "/"

            object_key = f"{prefix}{key}"
            await connection.delete_object(
                Bucket=bucket_name,
                Key=object_key,
            )
        except ClientError as e:
            raise InfrastructureError(str(e))

