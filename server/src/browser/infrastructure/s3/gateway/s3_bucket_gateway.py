import logging
from typing import List
from uuid import UUID

from botocore.exceptions import ParamValidationError, ClientError

from browser.application.common.gateway.s3_bucket_gateway import S3BucketGateway
from browser.domain.entity.s3_bucket import S3Bucket
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.infrastructure.exceptions.s3 import S3BucketCreationAccessDeniedError
from browser.infrastructure.s3.s3_connection_manager import AiobotocoreS3ConnectionManager

logger = logging.getLogger(__name__)

class AiobotocoreS3BucketGateway(S3BucketGateway):

    def __init__(self, connection_manager: AiobotocoreS3ConnectionManager) -> None:
        self._connection_manager = connection_manager



    async def create(
            self,
            connection_id: UUID,
            name: str
    ) -> None:

        connection = await self._connection_manager.get_active_connection(
            connection_id
        )

        if not connection:
            raise InfrastructureError(
                "Connection not found"
            )

        try:
            await connection.create_bucket(
                Bucket=name
            )
            return None
        except ParamValidationError as err:

            logger.error(err)

            raise InfrastructureError(
                "Invalid bucket parameters"
            )

        except ClientError as err:
            logger.error(err)
            error_code = err.response.get(
                "Error",
                {}
            ).get("Code")

            if error_code == "BucketAlreadyExists":
                raise InfrastructureError(
                    "Bucket already exists"
                )

            if error_code == "BucketAlreadyOwnedByYou":
                raise InfrastructureError(
                    "Bucket already owned by you"
                )

            if error_code == "InvalidBucketName":
                raise InfrastructureError(
                    "Invalid bucket name"
                )

            if error_code == "AccessDenied":
                raise S3BucketCreationAccessDeniedError

            raise InfrastructureError(str(err))

        except Exception as err:

            logger.error(err)

            raise InfrastructureError(str(err))


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


