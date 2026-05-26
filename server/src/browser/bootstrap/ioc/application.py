from dishka import Provider, Scope, provide_all, provide

from browser.application.buckets.read import ReadAllBucketsByConnectionId
from browser.application.common.gateway.s3_bucket_gateway import S3BucketGateway
from browser.application.common.gateway.s3_connection_settings_gateway import S3ConnectionSettingsGateway
from browser.application.common.gateway.s3_objects_gateway import S3ObjectsGateway
from browser.application.common.gateway.uow import UoW
from browser.application.objects.read import ReadAllObjects
from browser.application.s3_connections.create import CreateS3Connection
from browser.application.s3_connections.read import ReadActiveConnections
from browser.application.s3_connections.restore import RestoreS3Connection
from browser.application.s3_settings.delete import DeleteS3ConnectionSettingById
from browser.application.s3_settings.read import ReadS3SettingsAll, ReadS3ConnectionSettingByID
from browser.infrastructure.persistence.gateway.s3_connection_settings_gateway import SAS3ConnectionSettingsGateway
from browser.infrastructure.persistence.uow import SAUoW
from browser.infrastructure.s3.gateway.s3_bucket_gateway import AiobotocoreS3BucketGateway
from browser.infrastructure.s3.gateway.s3_objects_gateway import AiobotocoreS3ObjectsGateway


class ApplicationProvider(Provider):

    scope = Scope.REQUEST

    uow = provide(SAUoW, provides=UoW)

    cases = provide_all(
        CreateS3Connection,
        ReadS3SettingsAll,
        ReadS3ConnectionSettingByID,
        DeleteS3ConnectionSettingById,
        ReadActiveConnections,
        RestoreS3Connection,
        ReadAllBucketsByConnectionId,
        ReadAllObjects
    )

    s3_connection_settings_gateway = provide(SAS3ConnectionSettingsGateway, provides=S3ConnectionSettingsGateway)

    s3_bucket_gateway = provide(AiobotocoreS3BucketGateway, provides=S3BucketGateway)

    s3_objects_gateway = provide(AiobotocoreS3ObjectsGateway, provides=S3ObjectsGateway)
