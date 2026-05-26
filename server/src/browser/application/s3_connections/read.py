import logging
from typing import List

from browser.application.common.gateway.s3_connection_manager import S3ConnectionManager
from browser.domain.entity.s3_connection_config import ConnectionConfig

logger = logging.getLogger(__name__)

class ReadActiveConnections:

    def __init__(self, s3_connection_manager: S3ConnectionManager):
        self._s3_connection_manager = s3_connection_manager

    async def execute(self) -> List[ConnectionConfig]:
        logger.info("Start reading all active connections")

        result =  await self._s3_connection_manager.get_active_connections()

        logger.info("End reading all active connections")

        return result
