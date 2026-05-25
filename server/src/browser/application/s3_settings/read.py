import logging
from typing import List

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
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