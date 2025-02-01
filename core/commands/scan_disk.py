import os
import json
import ctypes
import logging
from pathlib import Path

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class ScanDiskCommand(ICommand):
    def __init__(self, disk_paths: list[str]) -> None:
        self.disk_paths: list[str] = disk_paths

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        disk_data: list = []
        for disk_path in self.disk_paths:
            data = self._get_disk_usage(disk_path)
            if data:
                disk_data.append(data)

        download_folder = Path.home() / "Downloads"
        output_file = download_folder / "disk_usage.json"
        self._save_to_json(disk_data, output_file)
        logging.info(f"Disk usage data saved to '{output_file}'")

    def _get_disk_usage(self, disk_path: str) -> dict | None:
        """
        Gets the disk usage information for a path.
        """
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        total_free_bytes = ctypes.c_ulonglong(0)

        if ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            disk_path,
            ctypes.byref(free_bytes),
            ctypes.byref(total_bytes),
            ctypes.byref(total_free_bytes),
        ):
            total_gb: float = total_bytes.value / (1024**3)
            free_gb: float = free_bytes.value / (1024**3)
            used_gb: float = total_gb - free_gb
            percent_used: float = (used_gb / total_gb) * 100

            volume_label, drive_name = self._get_volume_label_and_drive(disk_path)

            disk_info: dict = {
                "drive_name": drive_name,
                "volume_label": volume_label,
                "total": f"{total_gb:.0f} GB",
                "used": f"{used_gb:.0f} GB",
                "free": f"{free_gb:.0f} GB",
                "percent_used": f"{percent_used:.0f}%",
            }
            return disk_info

    def _get_volume_label_and_drive(self, disk_path: str) -> tuple:
        """
        Gets the volume label and the disk name.
        """
        volume_label = ctypes.create_unicode_buffer(255)
        file_system_name = ctypes.create_unicode_buffer(255)

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

    def _save_to_json(self, data: dict, output_file: Path) -> None:
        """
        Saves the results to a JSON file.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
