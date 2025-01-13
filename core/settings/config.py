"""
Config file.
"""

import os

from core.interfaces.config_interface import IConfig
from core.utils.exceptions import PathNotFound


class Config(IConfig):
    # Constants
    DIRECTORY: str = "D:\\Test"
    OUTPUT_FOLDER: str = "D:\\Downloads\\_OK"

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
