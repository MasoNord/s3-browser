import logging
from dataclasses import dataclass

import uuid6

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.uow import UoW
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting

logger = logging.getLogger(__name__)

@dataclass
class CreateS3SettingRequest:
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str

class CreateS3Setting:

    def __init__(
        self,
        s3_connection_settings_gateway: S3ConnectionSettingsGateway,
        uow: UoW
    ):
        self._s3_connection_settings_gateway = s3_connection_settings_gateway
        self._uow = uow

    async def execute(self, create_request: CreateS3SettingRequest) -> None:
        logger.info("Start creating new connection")

        connection_id = uuid6.uuid7()

        s3_connection_setting = S3ConnectionSetting(
            id=str(connection_id),
            region_name=create_request.region_name,
            endpoint_url=create_request.endpoint_url,
            aws_access_key_id=create_request.aws_access_key_id,
            aws_secret_access_key=create_request.aws_secret_access_key,
        )

        async with self._uow:
            await self._s3_connection_settings_gateway.add(s3_connection_setting)
            await self._uow.commit()

        logger.info("End creating new connection")
