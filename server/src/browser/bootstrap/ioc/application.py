from dishka import Provider, Scope, provide_all, provide

from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.s3_connections.create import CreateS3Connection
from browser.infrastructure.persistence.gateway.s3_connection_settings_gateway import SAS3ConnectionSettingsGateway


class ApplicationProvider(Provider):

    scope = Scope.REQUEST

    cases = provide_all(CreateS3Connection)

    s3_connection_settings_gateway = provide(SAS3ConnectionSettingsGateway, provides=S3ConnectionSettingsGateway)
