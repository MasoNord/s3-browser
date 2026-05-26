import logging
from uuid import UUID

from browser.application.common.gateway.s3_connection_manager import S3ConnectionManager
from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.exceptions.base import ApplicationError

logger = logging.getLogger(__name__)

class RestoreS3Connection:

    def __init__(self, s3_connection_manager: S3ConnectionManager, s3_settings_gateway: S3ConnectionSettingsGateway):
        self._s3_connection_manager = s3_connection_manager
        self._s3_settings_gateway = s3_settings_gateway

    async def execute(self, connection_id: UUID) -> None:
        logger.info("Start pinning s3 connection: Connection ID: %s", connection_id)

        setting = await self._s3_settings_gateway.get_by_id(str(connection_id))

        if not setting:
            logger.warning("S3 setting has not been found by Connection ID: %s", connection_id)
            raise ApplicationError

        await self._s3_connection_manager.restore_connection(connection_id, setting)

        logger.info("Ending pinning s3 connection")

        return None