from abc import ABC, abstractmethod


class IRepository(ABC):
    """
    Interface for repository class.
    """

    @abstractmethod
    def create(self, data: dict) -> None:
        pass

    @abstractmethod
    def exists(self, title: str) -> bool:
        pass
