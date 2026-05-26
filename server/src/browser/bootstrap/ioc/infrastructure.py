import logging
from typing import AsyncIterator

from aiobotocore.session import AioSession, get_session
from dishka import Provider, provide, Scope, AnyOf
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from browser.bootstrap.config.sqlite import LocalSQLLiteConnectionConfig
from browser.infrastructure.s3.s3_connection_manager import S3ConnectionManager, AiobotocoreS3ConnectionManager

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

    @provide(scope = Scope.APP)
    async def provide_s3_session(self) -> AioSession:
        logger.debug("Creating AioSession for S3 client")
        return get_session()

    @provide(scope=Scope.APP, provides=AnyOf[S3ConnectionManager, AiobotocoreS3ConnectionManager])
    async def provide_connection_manager(self, aiobotocore_session: AioSession) -> AsyncIterator[AiobotocoreS3ConnectionManager]:

        logger.debug("Starting S3 connection manager...")
        async with AiobotocoreS3ConnectionManager(aiobotocore_session) as connection_manager:
            logger.debug("S3 connection manager started.")
            yield connection_manager
            logger.debug("Closing S3 connection manager.")
        logger.debug("S3 connection manager closed.")


def infrastructure_providers() -> tuple[Provider, ...]:
    return (
        LocalSQLLiteConnectionProvider(),
        S3()
    )


