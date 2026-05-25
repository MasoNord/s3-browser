from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.infrastructure.exceptions.base import InfrastructureError


class SAS3ConnectionSettingsGateway(S3ConnectionSettingsGateway):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, instance: S3ConnectionSetting) -> None:
        try:
            self._session.add(instance)
            await self._session.flush((instance,))
        except IntegrityError as err:
            raise InfrastructureError from err

    async def delete(self, instance: S3ConnectionSetting) -> None:
        pass

    async def get_by_id(self, settings_id: UUID) -> S3ConnectionSetting:
        pass


    async def get_all(self) -> List[S3ConnectionSetting]:
        stmt = select(S3ConnectionSetting)

        records = await self._session.execute(stmt)

        connection_settings = records.scalars().all()

        return list(connection_settings)