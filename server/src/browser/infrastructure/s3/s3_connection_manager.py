import asyncio
import logging

from uuid import UUID
from typing import Self, Final, List
from datetime import datetime, timezone
from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession
from botocore.exceptions import UnknownServiceError

from browser.application.common.gateway.s3_connection_manager import S3ConnectionManager
from browser.domain.entity.s3_connection_config import ConnectionConfig
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.infrastructure.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

CONNECTION_IDLE_THRESHOLD: Final[int] = 15 # In minutes
SLEEP_TIME_FOR_IDLE_CONNECTION_REMOVAL: Final[int] = 15 # In seconds

# TODO: replace all infrastructure errors by corresponding case errors
class AiobotocoreS3ConnectionManager(S3ConnectionManager):

    def __init__(self, aiobotocore_session: AioSession) -> None:
        self._background_tasks = set()
        self._active_connections_config: dict[UUID, ConnectionConfig] = {}
        self._active_connections: dict[
            UUID,
            AioBaseClient
        ] = {}

        self._aiobotocore_session = aiobotocore_session
        self._create_background_task()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._close()

    async def get_active_connection(self, connection_id) -> AioBaseClient | None:
        await self.ping(connection_id)

        return self._active_connections.get(connection_id, None)

    async def get_active_connections(self) -> List[ConnectionConfig]:
        return [
            self._active_connections_config[key] for key in self._active_connections_config.keys()
        ]

    async def ping(self, connection_id: UUID) -> None:
        connection_config = self._active_connections_config.get(connection_id, None)

        if connection_config is not None:
            connection_config.last_used_at = datetime.now(tz=timezone.utc)

        return None

    async def restore_connection(self, connection_id: UUID, setting: S3ConnectionSetting) -> None:


        connection_config = self._active_connections_config.get(connection_id, None)
        active_connection = self._active_connections.get(connection_id, None)

        # Check if connection exists
        if connection_config and active_connection:
            return None

        self._active_connections_config.pop(connection_id, None)
        self._active_connections.pop(connection_id, None)

        config_connection = ConnectionConfig(
            id=connection_id,
            region_name=setting.region_name,
            endpoint_url=setting.endpoint_url,
            aws_access_key_id=setting.aws_access_key_id,
            aws_secret_access_key=setting.aws_secret_access_key,
            created_at=datetime.now(tz=timezone.utc),
            last_used_at=datetime.now(tz=timezone.utc)
        )

        await self.create_connection(config_connection)

        return None


    async def create_connection(self, config: ConnectionConfig) -> None:

        try:
            session = await self._aiobotocore_session.create_client(
                "s3",
                region_name=config.region_name,
                endpoint_url=config.endpoint_url,
                aws_access_key_id=config.aws_access_key_id,
                aws_secret_access_key=config.aws_secret_access_key,
            ).__aenter__()

            self._active_connections[config.id] = session
            self._active_connections_config[config.id] = config
            logger.info("Creating connection")
        except UnknownServiceError as err:
            raise InfrastructureError(str(err))

        return None

    async def disconnection_connection(self, connection_id: UUID) -> None:

        active_connection = self._active_connections.pop(connection_id, None)
        self._active_connections_config.pop(connection_id, None)

        if not active_connection:
            logger.warning("No active connection found by requested ID: %s", connection_id)
            return None
            # raise InfrastructureError()

        await active_connection.close()

        return None

    async def _remove_idle_connections_task(self) -> None:
        """
        Background task which removes idle connections. Connection is counted as IDLE if it's last_used_at property is
        greater than CONNECTION_IDLE_THRESHOLD
        :return:
        """

        try:
            while True:
                logger.info("Removing idle connections")
                await asyncio.sleep(15)

                for connection_id, connection in self._active_connections_config.items():
                    logger.info("Checking connection: Connection ID: %s", connection_id)
                    active_connection = self._active_connections.get(connection_id, None)
                    if active_connection:
                        logger.debug("Connection is found")
                        time_elapsed = datetime.now(tz=timezone.utc) - connection.last_used_at

                        time_elapsed_minutes = time_elapsed.total_seconds() / 60

                        logger.debug("Time elapsed since the last usage: %s minutes", time_elapsed_minutes)

                        if time_elapsed_minutes >= CONNECTION_IDLE_THRESHOLD:
                            logger.debug("Connection is idle. Closing connection...")
                            await active_connection.close()
                            self._active_connections_config.pop(connection_id, None)
                            logger.info("Connection has been closed")

        except asyncio.CancelledError:
            raise InfrastructureError()

    def _create_background_task(self) -> None:
        task = asyncio.create_task(self._remove_idle_connections_task())
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def _close(self) -> None:
        logger.info("Closing background tasks")

        for task in self._background_tasks:
            task.cancel()

        await asyncio.gather(
            *self._background_tasks,
            return_exceptions=True,
        )

        logger.info("Cleaning up background tasks set")
        self._background_tasks.clear()

        logger.info("Closing active connections")
        for connection_id, connection in self._active_connections.items():
            await connection.close()
            logger.info("Connection has been closed: Connection ID: %s", connection_id)
