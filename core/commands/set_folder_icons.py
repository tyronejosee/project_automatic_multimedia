import os
import logging
import subprocess

from core.interfaces.command_interface import ICommand
from core.utils.functions import get_type_choice
from core.utils.logging import setup_logging

setup_logging()


class SetFolderIcons(ICommand):
    def __init__(
        self,
        param: str,
        input_folder: str,
        icon_folder: str,
    ) -> None:
        self.param: str = param
        self.workspace_folder: str = input_folder
        self.icon_folder: str = icon_folder
        self.valid_params: list[str] = ["series", "movies"]

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        type_choice: str = get_type_choice(self.param, self.valid_params)
        for subfolder_name in os.listdir(self.workspace_folder):
            subfolder_path: str = os.path.join(
                self.workspace_folder,
                subfolder_name,
            )
            if os.path.isdir(subfolder_path):
                self._create_desktop_ini(
                    subfolder_path,
                    type_choice,
                    subfolder_name,
                )
                logging.info(f"Icon successfully configured {subfolder_path}")

    def _create_desktop_ini(
        self,
        folder_path: str,
        type_choice: str,
        icon_name: str,
    ) -> None:
        """
        Create a desktop.ini file for the folder with the appropriate icon.
        """
        desktop_ini_path: str = os.path.join(folder_path, "desktop.ini")
        icon_path: str = f"{self.icon_folder}\\{type_choice}\\{icon_name}.ico"

        lines: list[str] = [
            "[.ShellClassInfo]",
            f"IconResource={icon_path},0",
            "[ViewState]",
            "Mode=",
            "Vid=",
            "FolderType=Generic",
        ]

        with open(desktop_ini_path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")

        subprocess.run(["attrib", "+s", folder_path], shell=True)
        subprocess.run(["attrib", "+h", desktop_ini_path], shell=True)
