import logging
from dataclasses import dataclass
from uuid import UUID

import uuid6

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.uow import UoW
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.domain.exception.s3_setting import S3ConnectionSettingNotFoundError

logger = logging.getLogger(__name__)

@dataclass
class UpdateS3SettingRequest:
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


class UpdateS3Setting:

    def __init__(
        self,
        s3_connection_settings_gateway: S3ConnectionSettingsGateway,
        uow: UoW
    ):
        self._s3_connection_settings_gateway = s3_connection_settings_gateway
        self._uow = uow

    async def execute(self, setting_id: UUID, update_request: UpdateS3SettingRequest) -> S3ConnectionSetting:
        logger.info("Start updating connection: Setting ID: %s", setting_id)

        s3_setting = await self._s3_connection_settings_gateway.get_by_id(str(setting_id))

        if not s3_setting:
            raise S3ConnectionSettingNotFoundError

        s3_setting.region_name = update_request.region_name
        s3_setting.endpoint_url = update_request.endpoint_url
        s3_setting.aws_access_key_id = update_request.aws_access_key_id
        s3_setting.aws_secret_access_key = update_request.aws_secret_access_key

        await self._uow.commit()

        logger.info("End updating setting")

        return s3_setting