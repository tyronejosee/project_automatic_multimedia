"""
Config file.
"""

import os

from dotenv import load_dotenv

from core.interfaces.config_interface import IConfig
from core.utils.exceptions import PathNotFound

load_dotenv()


class Config(IConfig):
    # Constants
    DIRECTORY: str = "D:\\Workspaces"
    INPUT_FOLDER: str = "D:\\Downloads\\_OK"
    OUTPUT_FOLDER: str = "D:\\Downloads\\_OK"
    TEMP_FOLDER: str = "D:\\Downloads\\_OK\\temp"
    ICON_FOLDER: str = "C:\\Image"
    ANIME_URL: str = "https://myanimelist.net/anime/season"
    DISCORD_URL: str = os.getenv("DISCORD_URL", "")

    DESIRED_WIDTH: int = 256
    DESIRED_HEIGHT: int = 256

    SERIES_SIZE: tuple = (182, 256)
    MOVIES_SIZE: tuple = (165, 256)

    SUPPORTED_FORMATS: list = [".jpg", ".jpeg"]
    LIBRARY_PATHS: list = [
        "C:\\Archives\\Movies",
        "C:\\Archives\\Series",
        "D:\\Archives\\Movies",
        "D:\\Archives\\Series",
        "E:\\Archives\\Movies",
        "E:\\Archives\\Series",
        "F:\\Archives\\Movies",
        "F:\\Archives\\Series",
        "G:\\Archives\\Movies",
        "G:\\Archives\\Series",
        "H:\\Archives\\Movies",
        "H:\\Archives\\Series",
    ]
    CLEAN_FILES: list[str] = [
        ".info",
        "desktop.ini",
        "Thumbs.db",
        ".DS_Store",
    ]
    DISK_PATHS: list = [
        "A:\\",
        "C:\\",
        "D:\\",
        "E:\\",
        "F:\\",
        "G:\\",
        "H:\\",
    ]

    ELEMENTS_TO_SCRAPE: dict[str, str] = {
        "title_jpn": "h1.title-name.h1_bold_none > strong",
        "title_eng": "div.h1-title > div > p.title-english.title-inherit",
        "title_kanji": "div.spaceit_pad:-soup-contains('Japanese:')",
        "year": "div.spaceit_pad:-soup-contains('Premiered:') a",
        "og_image": 'meta[property="og:image"]',
        "website": "a.link.ga-click:has(div:-soup-contains('Official Site'))",
    }
    HEADERS_EN: dict[str, str] = {
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._validate()
        return cls._instance

    @classmethod
    def _validate(cls) -> None:
        """
        Validates the configuration values.
        Raises exceptions if invalid values are detected.
        """
        if not os.path.isdir(cls.DIRECTORY):
            raise PathNotFound(f"Path '{cls.DIRECTORY}' does not exists.")
        if not isinstance(cls.OUTPUT_FOLDER, str):
            raise TypeError("OUTPUT_FOLDER must be a str.")
