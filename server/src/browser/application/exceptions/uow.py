from browser.application.exceptions.base import ApplicationError


class FlushError(ApplicationError):
    pass

class CommitError(ApplicationError):
    pass

class RollbackError(ApplicationError):
    pass