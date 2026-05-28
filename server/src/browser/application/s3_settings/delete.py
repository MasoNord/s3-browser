import logging
from uuid import UUID

from browser.application.common.gateway.s3_connection_manager import S3ConnectionManager
from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.uow import UoW
from browser.application.exceptions.base import ApplicationError
from browser.domain.exception.s3_setting import S3ConnectionSettingNotFoundError

logger = logging.getLogger(__name__)


class DeleteS3ConnectionSettingById:

    def __init__(
        self,
        s3_connection_settings_gateway: S3ConnectionSettingsGateway,
        s3_connection_manager: S3ConnectionManager,
        uow: UoW
    ):
        self._s3_connection_settings_gateway = s3_connection_settings_gateway
        self._s3_connection_manager = s3_connection_manager
        self._uow = uow

    async def execute(self, setting_id: UUID) -> None:
        logger.info("Start deleting s3 connection setting: Setting ID: %s", setting_id)

        connection_setting = await self._s3_connection_settings_gateway.get_by_id(str(setting_id))

        if not connection_setting:
            raise S3ConnectionSettingNotFoundError

        async with self._uow:
            await self._s3_connection_manager.disconnection_connection(setting_id)
            await self._s3_connection_settings_gateway.delete(connection_setting)
            await self._uow.commit()

        logger.info("End deleting s3 connection setting")

        return None