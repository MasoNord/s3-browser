from dishka import Provider, Scope, provide_all, provide

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.uow import UoW
from browser.application.s3_connections.create import CreateS3Connection
from browser.application.s3_settings.read import ReadS3SettingsAll
from browser.infrastructure.persistence.gateway.s3_connection_settings_gateway import SAS3ConnectionSettingsGateway
from browser.infrastructure.persistence.uow import SAUoW


class ApplicationProvider(Provider):

    scope = Scope.REQUEST

    uow = provide(SAUoW, provides=UoW)

    cases = provide_all(
        CreateS3Connection,
        ReadS3SettingsAll

    )

    s3_connection_settings_gateway = provide(SAS3ConnectionSettingsGateway, provides=S3ConnectionSettingsGateway)
