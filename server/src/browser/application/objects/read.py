import logging
from uuid import UUID

from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway
from browser.application.objects.dto import ReadObject, ObjectFile, ObjectFolder

logger = logging.getLogger(__name__)

class ReadAllObjects:

    def __init__(self, s3_objects_gateway: S3ObjectsGateway):
        self._s3_objects_gateway = s3_objects_gateway

    async def execute(
        self,
        connection_id: UUID,
        bucket_name: str,
        prefix: str | None,
        delimiter: str = "/"
    ) -> ReadObject:

        logger.info("Start reading all objects")

        response = await self._s3_objects_gateway.get_objects(connection_id, bucket_name, prefix, delimiter)


        result = ReadObject(
            current_prefix=prefix,
            folders=list(),
            files=list()
        )

        if "CommonPrefixes" in response:
            for cp in response["CommonPrefixes"]:
                full_key = cp["Prefix"]
                name = full_key[len(prefix):]
                result.folders.append(ObjectFolder(name=name, full_key=full_key))

        if "Contents" in response:
            for obj in response["Contents"]:
                full_key = obj["Key"]

                if full_key == prefix:
                    continue

                name = full_key[len(prefix):]
                result.files.append(
                    ObjectFile(
                        name=name,
                        full_key=full_key,
                        size=obj["Size"],
                        last_modified=obj["LastModified"].isoformat() if hasattr(obj["LastModified"], "isoformat") else
                    obj["LastModified"]
                    )
                )

        logger.info("Finish reading all objects")

        return result