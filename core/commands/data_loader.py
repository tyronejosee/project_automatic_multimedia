import os
import json
import logging

from core.interfaces.command_interface import ICommand
from core.settings.database import Database
from core.utils.logging import setup_logging

setup_logging()


class DataLoaderCommand(ICommand):
    def __init__(
        self,
        param: str,
        icon_folder: str,
    ) -> None:
        self.param: str = param
        self.icon_folder: str = icon_folder
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

        records: list = self._scan_folder(self.icon_folder, self.param)
        new_records: list = [
            record
            for record in records
            if not type_repository.exists(title=record["title"])
        ]

        if new_records:
            type_repository.create_batch(new_records)
            logging.info(f"Records saved in db ({len(new_records)} items).")
            self._save_to_json(new_records, self.param)
        else:
            logging.info("No new records to add.")

    def _scan_folder(self, icon_folder: str, type_folder: str) -> list:
        """
        Scans a folder for files and generates a list with metadata.
        """
        files: list = []
        folder_name: str = f"{icon_folder}\\{type_folder.capitalize()}"

        for filename in os.listdir(folder_name):
            filepath: str = os.path.join(folder_name, filename)

            if os.path.isfile(filepath):
                data: dict[str, str | int] = {
                    "title": filename.replace(".ico", ""),
                    "is_available": 1,
                }
                files.append(data)
        return files

    def _save_to_json(self, records: list, type: str) -> None:
        """
        Saves a list of dictionaries to a JSON file.
        """
        if not isinstance(records, list):
            raise ValueError("Expected a list of dictionaries.")
        if not all(isinstance(record, dict) for record in records):
            raise ValueError("All elements in the list must be dictionaries.")
        with open(f"{type}.json", "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=4)
            logging.info(
                f"Records saved in {type}.json ({len(records)}) items.",
            )
