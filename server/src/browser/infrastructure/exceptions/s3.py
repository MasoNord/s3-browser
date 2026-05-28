from browser.infrastructure.exceptions.base import InfrastructureError


class S3ConnectionError(InfrastructureError):
    """Base S3 connection error"""


class S3ClientCreationError(S3ConnectionError):
    """Failed to create S3 client"""


class S3UnknownServiceError(S3ConnectionError):
    """Unknown S3 service"""


class S3ConnectionNotFoundError(S3ConnectionError):
    """S3 connection not found"""


class S3ConnectionCloseError(S3ConnectionError):
    """Failed to close S3 connection"""


class S3ConnectionRestoreError(S3ConnectionError):
    """Failed to restore S3 connection"""


class S3IdleConnectionCleanupError(S3ConnectionError):
    """Failed during idle connection cleanup"""


class S3BackgroundTaskError(S3ConnectionError):
    """Background task failure"""


class S3PingError(S3ConnectionError):
    """Failed to ping S3 connection"""


class S3InvalidConnectionConfigError(S3ConnectionError):
    """Invalid S3 connection config"""

class S3BucketCreationAccessDeniedError(S3ConnectionError):
    """Missing S3 bucket creation access denied"""

class ActionConnectionNotFoundById(InfrastructureError):
    """Failed to get active S3 connection"""