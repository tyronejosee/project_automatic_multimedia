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

    @property
    @abstractmethod
    def ANIME_URL(self) -> str:
        pass

    @property
    @abstractmethod
    def ELEMENTS_TO_SCRAPE(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def HEADERS_EN(self) -> dict[str, str]:
        pass

    @classmethod
    @abstractmethod
    def _validate(cls) -> None:
        pass
