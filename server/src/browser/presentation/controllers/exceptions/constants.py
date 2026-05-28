from browser.application.exceptions.base import ApplicationError
from browser.application.exceptions.uow import CommitError, RollbackError, FlushError
from browser.domain.exception.base import DomainError
from browser.domain.exception.s3_setting import S3ConnectionSettingNotFoundError
from browser.infrastructure.exceptions.base import InfrastructureError
from browser.infrastructure.exceptions.s3 import S3ConnectionError, S3ClientCreationError, S3UnknownServiceError, \
    S3ConnectionNotFoundError, S3ConnectionCloseError, S3ConnectionRestoreError, S3IdleConnectionCleanupError, \
    S3BackgroundTaskError, S3PingError, S3InvalidConnectionConfigError, S3BucketCreationAccessDeniedError

ERROR_HTTP_CODE = {

    ApplicationError: 500,
    InfrastructureError: 500,
    DomainError: 500,

    CommitError: 500,
    FlushError: 500,
    RollbackError: 500,


    S3ConnectionError: 500,
    S3ClientCreationError: 500,
    S3UnknownServiceError: 500,
    S3ConnectionNotFoundError: 404,
    S3ConnectionSettingNotFoundError: 404,
    S3ConnectionCloseError: 500,
    S3ConnectionRestoreError: 500,
    S3IdleConnectionCleanupError: 500,
    S3BackgroundTaskError: 500,
    S3PingError: 500,
    S3InvalidConnectionConfigError: 400,

    S3BucketCreationAccessDeniedError: 403,

    Exception: 500
}

ERROR_MESSAGE = {

    ApplicationError: "Unhandled application error",
    InfrastructureError: "Unhandled infrastructure error",
    DomainError: "Unhandled domain error",

    CommitError: "Unhandled commit error",
    FlushError: "Unhandled flush error",
    RollbackError: "Unhandled rollback error",

    S3BucketCreationAccessDeniedError: "S3 bucket creation access denied error",
    S3ConnectionError: "Unhandled S3 connection error",
    S3ClientCreationError: "Failed to create S3 connection",
    S3ConnectionSettingNotFoundError: "S3 connection setting not found error",
    S3UnknownServiceError: "Unknown S3 service",
    S3ConnectionNotFoundError: "S3 connection not found",
    S3ConnectionCloseError: "Failed to close S3 connection",
    S3ConnectionRestoreError: "Failed to restore S3 connection",
    S3IdleConnectionCleanupError: "Failed to cleanup idle connections",
    S3BackgroundTaskError: "Background task failure",
    S3PingError: "Failed to ping S3 connection",
    S3InvalidConnectionConfigError: "Invalid S3 connection config",

    Exception: "Unhandled exception"
}

ERROR_CODE = {

    ApplicationError: "APPLICATION_ERROR",
    InfrastructureError: "INFRASTRUCTURE_ERROR",
    DomainError: "DOMAIN_ERROR",

    CommitError: "COMMIT_ERROR",
    FlushError: "FLUSH_ERROR",
    RollbackError: "ROLLBACK_ERROR",

    S3BucketCreationAccessDeniedError: "S3_BUCKET_CREATION_ACCESS_DENIED_ERROR",
    S3ConnectionError: "S3_CONNECTION_ERROR",
    S3ConnectionSettingNotFoundError: "S3_CONNECTION_SETTING_NOT_FOUND",
    S3ClientCreationError: "S3_CLIENT_CREATION_ERROR",
    S3UnknownServiceError: "S3_UNKNOWN_SERVICE_ERROR",
    S3ConnectionNotFoundError: "S3_CONNECTION_NOT_FOUND",
    S3ConnectionCloseError: "S3_CONNECTION_CLOSE_ERROR",
    S3ConnectionRestoreError: "S3_CONNECTION_RESTORE_ERROR",
    S3IdleConnectionCleanupError: "S3_IDLE_CONNECTION_CLEANUP_ERROR",
    S3BackgroundTaskError: "S3_BACKGROUND_TASK_ERROR",
    S3PingError: "S3_PING_ERROR",
    S3InvalidConnectionConfigError: "S3_INVALID_CONNECTION_CONFIG",

    Exception: "UNHANDLED_EXCEPTION"
}