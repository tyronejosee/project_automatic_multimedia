import os
import re
import json
import logging
import ctypes
from datetime import datetime, timezone
from pathlib import Path

from slugify import slugify

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class ScanLibraryCommand(ICommand):
    def __init__(self, library_paths: list[str]) -> None:
        self.library_paths: list[str] = library_paths

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        for library_path in self.library_paths:
            data: list[dict] = self._scan_folders([library_path])
            if data:
                folder: Path = Path.home() / "Downloads"
                filename: str = slugify(data[0]["location"])
                type_content: str = slugify(data[0]["type"])
                output_file: Path = folder / f"{filename}-{type_content}.json"
                self._save_results_to_json(output_file, data)
                logging.info(f"Data saved to '{output_file}'")

    def _scan_folders(self, library_paths: list[str]) -> list[dict]:
        """
        Scans folders and retrieves relevant information.
        """
        results: list = []
        existing_paths: list[str] = self._check_paths_exist(library_paths)

        match: re.Match[str] | None = re.match(r"^[A-Z]:\\", library_paths[0])
        disk: str = match.group(0) if match else ""
        volume_label, _ = self._get_volume_label_and_drive(disk)

        for base_path in existing_paths:
            type_folder: str = os.path.basename(base_path)
            for genre in os.listdir(base_path):
                genre_path: str = os.path.join(base_path, genre)
                if os.path.isdir(genre_path):
                    for folder in os.listdir(genre_path):
                        folder_slug: str = slugify(folder)
                        folder_name: str = re.sub(r" \((\d{4})\)", "", folder)
                        folder_name: str = re.sub(r"_ ", ": ", folder_name)
                        match = re.search(r"\((\d{4})\)", folder)
                        year: str = match.group(1) if match else "0000"
                        movie_path: str = os.path.join(genre_path, folder)
                        if os.path.isdir(movie_path):
                            (
                                file_name,
                                file_size,
                                has_file,
                                created_at,
                                updated_at,
                            ) = self._get_video_or_image(movie_path)
                            results.append(
                                {
                                    "folder_name": folder_name,
                                    "file_name": file_name,
                                    "file_size": file_size,
                                    "year": year,
                                    "slug": folder_slug,
                                    "image": f"/{type_folder.lower()}/{folder_slug}.webp",
                                    "genre": genre,
                                    "type": type_folder,
                                    "has_file": has_file,
                                    "location": volume_label,
                                    "created_at": created_at or "Unknown",
                                    "updated_at": updated_at or "Unknown",
                                }
                            )
        return results

    def _check_paths_exist(self, paths: list[str]) -> list[str]:
        """
        Checks which paths exist and returns a list of valid paths.
        """
        return [path for path in paths if os.path.exists(path)]

    def _get_video_or_image(self, folder_path: str) -> tuple[
        str,
        str,
        bool,
        str,
        str,
    ]:
        """
        Searches for a video or image file in the folder
        and retrieves its metadata.
        """
        video_extensions: set[str] = {"mkv", "mp4"}
        image_extensions: set[str] = {"jpg"}
        has_file = False
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
                    file_name = re.sub(
                        r" - 01\.(mkv|mp4|avi)$",
                        "",
                        file,
                    ).strip()
                    file_name = re.sub(r"_ ", ": ", file_name)
                    file_size = f"{file_size_in_gb:.2f} GB"
                    has_file = True
                    created_at: str = datetime.fromtimestamp(
                        file_creation_time, timezone.utc
                    ).strftime("%d-%m-%Y")
                    updated_at: str = datetime.fromtimestamp(
                        file_modification_time, timezone.utc
                    ).strftime("%d-%m-%Y")

                    base_name: str = os.path.splitext(file)[0]
                    for image_ext in image_extensions:
                        image_file: str = base_name + "." + image_ext
                        image_path: str = os.path.join(folder_path, image_file)
                        if os.path.exists(image_path):
                            break

                    break

                elif ext in image_extensions and not has_file:
                    file_name: str = file.replace("- Cover.jpg", "").strip()
                    file_name = re.sub(r"_ ", ": ", file_name)
                    file_size: str = f"{file_size_in_gb:.2f} GB"

                    if created_at is None:
                        created_at: str = datetime.fromtimestamp(
                            file_creation_time, timezone.utc
                        ).strftime("%d-%m-%Y")
                    if updated_at is None:
                        updated_at: str = datetime.fromtimestamp(
                            file_modification_time, timezone.utc
                        ).strftime("%d-%m-%Y")

        return (
            file_name,
            file_size,
            has_file,
            created_at,
            updated_at,
        )

    def _get_volume_label_and_drive(self, disk_path: str) -> tuple:
        """
        Gets the volume label and the disk name.
        """
        volume_label: ctypes.Array = ctypes.create_unicode_buffer(255)
        file_system_name: ctypes.Array = ctypes.create_unicode_buffer(255)

        result = ctypes.windll.kernel32.GetVolumeInformationW(
            disk_path,
            volume_label,
            len(volume_label),
            None,
            None,
            None,
            file_system_name,
            len(file_system_name),
        )

        if result != 0:
            volume_label_str = volume_label.value if volume_label.value else "No label"
        else:
            volume_label_str = "No label"

        drive_name: str = os.path.splitdrive(disk_path)[0]
        return volume_label_str, drive_name

    def _save_results_to_json(
        self,
        output_file: Path,
        data: list[dict],
    ) -> None:
        """
        Saves the results to a JSON file.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
