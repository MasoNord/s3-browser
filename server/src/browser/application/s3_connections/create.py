import logging
from dataclasses import dataclass
from datetime import datetime, timezone

import uuid6

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.uow import UoW
from browser.domain.entity.s3_connection_config import ConnectionConfig
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.infrastructure.s3.s3_connection_manager import S3ConnectionManager

logger = logging.getLogger(__name__)

@dataclass
class CreateS3ConnectionRequest:
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


class CreateS3Connection:

    def __init__(
        self,
        s3_connection_settings_gateway: S3ConnectionSettingsGateway,
        s3_connection_manager: S3ConnectionManager,
        uow: UoW
    ):
        self._s3_connection_settings_gateway = s3_connection_settings_gateway
        self._s3_connection_manager = s3_connection_manager
        self._uow = uow

    async def execute(self, create_request: CreateS3ConnectionRequest):
        logger.info("Start creating new connection")

        connection_id = uuid6.uuid7()
        config_connection = ConnectionConfig(
            id=connection_id,
            region_name=create_request.region_name,
            endpoint_url=create_request.endpoint_url,
            aws_access_key_id=create_request.aws_access_key_id,
            aws_secret_access_key=create_request.aws_secret_access_key,
            created_at=datetime.now(tz=timezone.utc),
            last_used_at=datetime.now(tz=timezone.utc)
        )

        s3_connection_setting = S3ConnectionSetting(
            id=str(connection_id),
            region_name=create_request.region_name,
            endpoint_url=create_request.endpoint_url,
            aws_access_key_id=create_request.aws_access_key_id,
            aws_secret_access_key=create_request.aws_secret_access_key,
        )


        async with self._uow:
            await self._s3_connection_settings_gateway.add(s3_connection_setting)
            await self._s3_connection_manager.create_connection(config_connection)
            await self._uow.commit()

        logger.info("End creating new connection")