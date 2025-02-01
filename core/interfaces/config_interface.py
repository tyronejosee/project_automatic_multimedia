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
    def INPUT_FOLDER(self) -> str:
        pass

    @property
    @abstractmethod
    def OUTPUT_FOLDER(self) -> str:
        pass

    @property
    @abstractmethod
    def TEMP_FOLDER(self) -> str:
        pass

    @property
    @abstractmethod
    def ICON_FOLDER(self) -> str:
        pass

    @property
    @abstractmethod
    def ANIME_URL(self) -> str:
        pass

    @property
    @abstractmethod
    def DESIRED_WIDTH(self) -> int:
        pass

    @property
    @abstractmethod
    def DESIRED_HEIGHT(self) -> int:
        pass

    @property
    @abstractmethod
    def SERIES_SIZE(self) -> tuple:
        pass

    @property
    @abstractmethod
    def MOVIES_SIZE(self) -> tuple:
        pass

    @property
    @abstractmethod
    def SUPPORTED_FORMATS(self) -> list:
        pass

    @property
    @abstractmethod
    def LIBRARY_PATHS(self) -> list:
        pass

    @property
    @abstractmethod
    def DISK_PATHS(self) -> list:
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
