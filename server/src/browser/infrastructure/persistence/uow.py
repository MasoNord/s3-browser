import logging
from typing import List, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from browser.application.common.gateway.uow import UoW
from browser.application.exceptions.uow import CommitError, FlushError

logger = logging.getLogger(__name__)

class SAUoW(UoW):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> "UoW":
        pass

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._session.rollback()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            logger.error("Unhandled commit error: %s", str(err))
            raise CommitError from err


    async def flush(self, objects: List[Any] | None) -> None:
        try:
            await self._session.flush(objects)
        except SQLAlchemyError as err:
            logger.error("Unhandled flush error: %s", str(err))
            raise FlushError from err


    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            logger.error("Unhandled rollback error: %s", str(err))
            raise CommitError from err