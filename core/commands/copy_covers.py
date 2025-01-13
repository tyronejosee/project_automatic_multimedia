import os
import shutil

from core.interfaces.command_interface import ICommand


class CopyCoversCommand(ICommand):
    def __init__(self, directory: str, output_folder: str) -> None:
        self.directory: str = directory
        self.output_folder: str = output_folder

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        cover_files: list[str] = self._find_cover_files()
        if not cover_files:
            raise FileNotFoundError("No .jpg files found.")

        # Ensure the output directory exists
        os.makedirs(self.output_folder, exist_ok=True)

        for cover in cover_files:
            self._process_cover_file(cover)

    def _find_cover_files(self) -> list[str]:
        """
        pending.
        """
        cover_files: list[str] = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith("- cover.jpg"):
                    cover_files.append(os.path.join(root, file))
        return cover_files

    def _process_cover_file(self, file: str) -> None:
        """
        pending.
        """
        try:
            parent_folder: str = os.path.basename(os.path.dirname(file))
            new_file_name: str = f"{parent_folder}.jpg"
            new_file_path: str = os.path.join(
                self.output_folder,
                new_file_name,
            )
            shutil.copy(file, new_file_path)
            print(f"Processing: {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
