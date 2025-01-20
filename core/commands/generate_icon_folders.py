import os
import logging

from core.interfaces.command_interface import ICommand
from core.settings.database import Database
from core.utils.logging import setup_logging

setup_logging()


class GenerateIconFoldersCommand(ICommand):
    def __init__(
        self,
        param: str,
        input_folder: str,
    ) -> None:
        self.param: str = param
        self.input_folder: str = input_folder
        self.valid_params: list[str] = ["series", "movies"]

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        database = Database()

        type_repository = {
            "movies": database.get_movie_repository(),
            "series": database.get_serie_repository(),
        }.get(self.param, "")

        if self.param not in self.valid_params:
            raise ValueError(f"Invalid type choice '{self.param}'")

        data_list: list[dict] = type_repository.get_all()

        if not data_list:
            logging.error("No data found in the database.")
            return

        for data in data_list:
            folder_name: str = self._sanitize_title(data["title"])
            folder_path: str = os.path.join(self.input_folder, folder_name)
            self._create_folder(folder_path)

    def _create_folder(self, folder_path: str) -> None:
        """
        Creates a folder at the specified path.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created folder {folder_path}.")
        except OSError as e:
            logging.error(f"Error creating folder {folder_path}: {e}.")

    def _sanitize_title(self, title: str) -> str:
        """
        Sanitizes the given title to make it safe for use as a folder name.
        """
        invalid_chars = "<>:" "/\\|?*"
        for char in invalid_chars:
            title = title.replace(char, "_")
        return title.strip()
