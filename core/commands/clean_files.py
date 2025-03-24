import os
import logging

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class CleanFilesCommand(ICommand):
    def __init__(self, directory: str, clean_files: list[str]) -> None:
        self.directory: str = directory
        self.clean_files: list[str] = clean_files

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        files: list[str] = self._find_files()
        if not files:
            raise FileNotFoundError("No files found.")

        for file in files:
            try:
                os.remove(file)
                logging.info(f"Deleted {file}")
            except Exception as e:
                logging.error({e})

    def _find_files(self) -> list[str]:
        """
        Finds files in the directory.
        """
        files: list[str] = []
        is_first_file: bool = False
        for root, _, archives in os.walk(self.directory):
            for archive in archives:
                full_path: str = os.path.join(root, archive)
                if archive in self.clean_files:
                    if is_first_file:
                        files.append(full_path)
                    is_first_file = True
        return files
