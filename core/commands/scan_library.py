import os
import json
# import logging
from datetime import datetime
from pathlib import Path

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class ScanLibraryCommand(ICommand):
    def __init__(self, disk_paths: list[str]) -> None:
        self.disk_paths: list[str] = disk_paths

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        data: list[dict] = self._scan_folders(self.disk_paths)
        self._save_results_to_json(data)

    def _scan_folders(self, disk_paths: list[str]) -> list[dict]:
        """Scans folders and retrieves relevant information."""
        results: list = []
        existing_paths: list[str] = self._check_paths_exist(disk_paths)

        for base_path in existing_paths:
            type_folder: str = os.path.basename(base_path)
            for genre in os.listdir(base_path):
                genre_path: str = os.path.join(base_path, genre)
                if os.path.isdir(genre_path):
                    for folder in os.listdir(genre_path):
                        movie_path: str = os.path.join(genre_path, folder)
                        if os.path.isdir(movie_path):
                            file_name, file_size, file_format, has_file, has_image, created_at, updated_at = (
                                self._get_video_or_image(movie_path)
                            )
                            results.append(
                                {
                                    "folder_name": folder,
                                    "file_name": file_name,
                                    "file_size": file_size,
                                    "genre": genre,
                                    "type": type_folder,
                                    "file_format": file_format,
                                    "has_file": has_file,
                                    "has_image": has_image,
                                    "created_at": created_at if created_at else "Unknown",
                                    "updated_at": updated_at if updated_at else "Unknown",
                                }
                            )
        return results

    def _check_paths_exist(self, paths: list[str]) -> list[str]:
        """
        Checks which paths exist and returns a list of valid paths.
        """
        return [path for path in paths if os.path.exists(path)]

    def _get_video_or_image(self, folder_path: str) -> tuple[str, str, str, bool, bool, str, str]:
        """
        Searches for a video or image file in the folder
        and retrieves its metadata.
        """
        video_extensions: set[str] = {"mkv", "mp4"}
        image_extensions: set[str] = {"jpg"}
        has_file = False
        has_image = False
        created_at = None
        updated_at = None

        for file in os.listdir(folder_path):
            file_path: str = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                ext: str = file.split(".")[-1].lower()
                file_creation_time: float = os.path.getctime(file_path)
                file_modification_time: float = os.path.getmtime(file_path)
                file_size_in_gb: float = os.path.getsize(file_path) / (1024**3)

                if ext in video_extensions:
                    file_name = file
                    file_size = f"{file_size_in_gb:.2f} GB"
                    file_format = ext
                    has_file = True
                    created_at = datetime.utcfromtimestamp(file_creation_time).isoformat()
                    updated_at = datetime.utcfromtimestamp(file_modification_time).isoformat()

                    base_name: str = os.path.splitext(file)[0]
                    for image_ext in image_extensions:
                        image_file: str = base_name + '.' + image_ext
                        image_path: str = os.path.join(folder_path, image_file)
                        if os.path.exists(image_path):
                            has_image = True
                            break

                    break

                elif ext in image_extensions and not has_file:
                    file_name: str = file
                    file_size: str = f"{file_size_in_gb:.2f} GB"
                    file_format: str = ext
                    has_image = True

                    if created_at is None:
                        created_at: str = datetime.utcfromtimestamp(file_creation_time).isoformat()
                    if updated_at is None:
                        updated_at: str = datetime.utcfromtimestamp(file_modification_time).isoformat()

        return (
            file_name,
            file_size,
            file_format,
            has_file,
            has_image,
            created_at,
            updated_at
        )

    def _save_results_to_json(self, data: list[dict]) -> None:
        """
        Saves the results to a JSON file.
        """
        desktop: Path = Path.home() / "Downloads"
        output_file: Path = desktop / "metadata.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
