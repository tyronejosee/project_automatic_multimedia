from abc import ABC, abstractmethod


class IConfig(ABC):
    """
    Interface for config class.
    """

    @property
    @abstractmethod
    def DIRECTORY(self) -> str:
        pass

    @property
    @abstractmethod
    def OUTPUT_FOLDER(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def _validate(cls) -> None:
        pass
