from abc import abstractmethod
from typing import Protocol
from uuid import UUID
from browser.domain.entity.s3_connection_config import ConnectionConfig


class S3ConnectionManager(Protocol):

    """Class for creating, deleting and fetching S3 connections"""

    @abstractmethod
    async def create_connection(self, config: ConnectionConfig) -> None:
        pass

    @abstractmethod
    async def disconnection_connection(self, connection_id: UUID) -> None:
        pass
