import logging
from typing import List
from uuid import UUID

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.exceptions.base import ApplicationError
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting

logger = logging.getLogger(__name__)

class ReadS3SettingsAll:

    def __init__(self, s3_connection_settings_gateway: S3ConnectionSettingsGateway):
        self.s3_connection_settings_gateway = s3_connection_settings_gateway

    async def execute(self) -> List[S3ConnectionSetting]:
        logger.info("Start reading all S3 connection settings")

        result = await self.s3_connection_settings_gateway.get_all()

        logger.info("Finish reading all S3 connection settings")

        return result

class ReadS3ConnectionSettingByID:

    def __init__(self, s3_connection_settings_gateway: S3ConnectionSettingsGateway):
        self.s3_connection_settings_gateway = s3_connection_settings_gateway

    async def execute(self, settings_id: UUID) -> S3ConnectionSetting:
        logger.info("Start reading S3 connection setting by ID: %s", settings_id)

        result = await self.s3_connection_settings_gateway.get_by_id(str(settings_id))

        # TODO: replace generic exception by specific one
        if not result:
            logger.warning("S3 connection setting not found for ID: %s", settings_id)
            raise ApplicationError

        logger.info("Finish reading S3 connection setting")

        return result