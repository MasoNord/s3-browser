from abc import abstractmethod
from typing import Protocol, List
from uuid import UUID
from browser.domain.entity.s3_connection_config import ConnectionConfig
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting


class S3ConnectionManager(Protocol):

    """Class for creating, deleting and fetching S3 connections"""

    @abstractmethod
    async def create_connection(self, config: ConnectionConfig) -> None:
        """
        Method to create new S3 connection
        :param config: necessary information to create a new connection
        :return:
        """

        raise NotImplementedError

    @abstractmethod
    async def disconnection_connection(self, connection_id: UUID) -> None:
        """
        Method to disconnect connection
        :param connection_id:
        :return:
        """

        raise NotImplementedError

    @abstractmethod
    async def ping(self, connection_id: UUID) -> None:
        """
        Method to update last_used_at property for the chosen connection
        :param connection_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def restore_connection(self, connection_id: UUID, setting: S3ConnectionSetting) -> None:
        """
        Method to restore connection
        :param connection_id:
        :param setting:
        :return:
        """

        raise NotImplementedError

    @abstractmethod
    async def get_active_connections(self) -> List[ConnectionConfig]:
        raise NotImplementedError
