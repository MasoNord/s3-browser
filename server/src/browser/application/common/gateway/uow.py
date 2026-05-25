from abc import abstractmethod
from typing import Protocol, Any, List


class UoW(Protocol):

    @abstractmethod
    async def __aenter__(self) -> "UoW":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self, objects: List[Any] | None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError