from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


class SAS3ConnectionSettingsGateway(S3ConnectionSettingsGateway):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, instance: S3ConnectionSetting) -> None:
        pass

    async def delete(self, instance: S3ConnectionSetting) -> None:
        pass

    async def get_by_id(self, settings_id: UUID) -> S3ConnectionSetting:
        pass


    async def get_all(self, settings_id: UUID) -> List[S3ConnectionSetting]:
        pass