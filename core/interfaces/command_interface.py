from abc import ABC, abstractmethod


class ICommand(ABC):
    """
    Interface for command class.
    """

    @abstractmethod
    def execute(self) -> None:
        pass
