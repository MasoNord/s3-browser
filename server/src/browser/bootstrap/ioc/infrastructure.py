import logging
from typing import AsyncIterator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from browser.bootstrap.config.sqlite import LocalSQLLiteConnectionConfig
from browser.domain.entity.s3_connection_settings import S3ConnectionSetting
from browser.infrastructure.s3.s3_connection_manager import S3ConnectionManager

logger = logging.getLogger(__name__)


class LocalSQLLiteConnectionProvider(Provider):


    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        sqlite: LocalSQLLiteConnectionConfig
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=sqlite.connection_url
        )

        logger.debug("Local async engine created with connection: %s", sqlite.connection_url)
        yield async_engine
        logger.debug("Disposing async engine...")
        await async_engine.dispose()
        logger.debug("Engine is disposed")

    @provide(scope=Scope.APP)
    def provide_async_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False
        )
        logger.debug("Async session maker initialized")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_main_async_session(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:

        logger.debug("Starting Main async session...")
        async with async_session_factory() as session:
            logger.debug("Main async session started.")
            yield session
            logger.debug("Closing Main async session.")
        logger.debug("Main async session closed.")


class S3(Provider):
    scope = Scope.APP

    connection_manager = provide(S3ConnectionManager)


def infrastructure_providers() -> tuple[Provider, ...]:
    return (
        LocalSQLLiteConnectionProvider(),
        S3()
    )


