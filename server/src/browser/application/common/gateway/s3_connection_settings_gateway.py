from abc import abstractmethod
from typing import Protocol, List
from uuid import UUID

from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


class S3ConnectionSettingsGateway(Protocol):

    """Class for creating, reading and deleting S3 connection settings."""

    @abstractmethod
    async def add(self, instance: S3ConnectionSetting) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance: S3ConnectionSetting) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, settings_id: UUID) -> S3ConnectionSetting:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[S3ConnectionSetting]:
        raise NotImplementedError