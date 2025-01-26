from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Interface for Observer pattern.
    """

    @abstractmethod
    def update(self, message: str) -> None:
        pass
