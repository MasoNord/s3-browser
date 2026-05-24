from dataclasses import dataclass

from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ConnectionConfig:
    pass

class S3ConnectionManager:
    """Class for creating, deleting and fetching S3 connections"""

    async def create_connection(self, config: ConnectionConfig) -> None:
        pass

    async def disconnection_connection(self, connection_id: UUID) -> None:
        pass
