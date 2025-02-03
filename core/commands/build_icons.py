import os
import shutil
import logging

from PIL import Image

from core.interfaces.command_interface import ICommand
from core.utils.exceptions import CommandNotFound
from core.utils.logging import setup_logging

setup_logging()


class BuildIconsCommand(ICommand):
    def __init__(
        self,
        param: str,
        series_size: tuple,
        movies_size: tuple,
        input_folder: str,
        temp_folder: str,
        output_folder: str,
        icon_folder: str,
        desired_width: int,
        desired_height: int,
        supported_formats: list,
    ) -> None:
        self.param: str = param
        self.series_size: tuple = series_size
        self.movies_size: tuple = movies_size
        self.input_folder: str = input_folder
        self.temp_folder: str = temp_folder
        self.output_folder: str = output_folder
        self.icon_folder: str = icon_folder
        self.desired_width: int = desired_width
        self.desired_height: int = desired_height
        self.supported_formats: list = supported_formats
        self.valid_params: list[str] = ["series", "movies"]

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        chosen_size = {
            "series": self.series_size,
            "movies": self.movies_size,
        }.get(self.param)

        if chosen_size is None:
            logging.info("Invalid choice.")
            return

        type_choice: str = self._get_type_choice()
        icon_path: str = f"{self.icon_folder}\\{type_choice}"

        self._process_images(
            chosen_size,
            self.input_folder,
            self.temp_folder,
            icon_path,
        )
        logging.info("Completed.")
        shutil.rmtree(self.temp_folder)

    def _process_images(
        self,
        size: tuple,
        input_folder: str,
        temp_folder: str,
        icon_path: str,
    ) -> None:
        """
        Processes each JPG img in input folder, resizing and converting to PNG.
        """
        self._ensure_folder_exists(temp_folder)
        self._ensure_folder_exists(icon_path)

        for filename in os.listdir(input_folder):
            if self._is_supported_image(filename):
                input_path: str = os.path.join(input_folder, filename)
                temp_path: str = os.path.join(
                    temp_folder, os.path.splitext(filename)[0] + ".png"
                )
                self._resize_image(input_path, temp_path, size)
                output_path: str = os.path.join(
                    icon_path, os.path.splitext(filename)[0] + ".ico"
                )
                self._add_transparent_space(temp_path, output_path)
            else:
                logging.error(f"Ignore (Not supported): {filename}")

    def _resize_image(
        self,
        image_path: str,
        output_path: str,
        size: tuple,
    ) -> None:
        """
        Resizes a JPG image to the specified dimensions and saves it as PNG.
        """
        logging.info(f"Resizing {image_path}")
        try:
            img: Image.Image = Image.open(image_path).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            img.save(output_path, format="PNG")
            logging.info(f"Save resized {output_path}")
        except Exception as e:
            logging.error(f"Error resizing {image_path}: {e}")

    def _add_transparent_space(
        self,
        image_path: str,
        output_path: str,
    ) -> None:
        """
        Adds transparent space to an image and saves it in ICO format.
        """
        logging.info(f"Process {image_path}")
        try:
            img: Image.Image = Image.open(image_path).convert("RGBA")
            original_width, original_height = img.size
            new_img: Image.Image = Image.new(
                "RGBA",
                (self.desired_width, self.desired_height),
                (0, 0, 0, 0),
            )
            left: int = (self.desired_width - original_width) // 2
            top: int = (self.desired_height - original_height) // 2
            new_img.paste(img, (left, top))
            new_img.save(output_path, format="ICO", sizes=[(256, 256)])
            logging.info(f"Save {output_path}")
        except FileNotFoundError:
            logging.error(f"File not found {output_path}")
        except Exception as e:
            logging.error(f"Could not process {image_path}: {e}")

    def _ensure_folder_exists(self, folder_path: str) -> None:
        """
        Ensures the specified folder exists; creates it if it does not.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _get_type_choice(self) -> str:
        """
        Returns the folder type based on the parameter.
        """
        if self.param == "Unknown":
            raise CommandNotFound("Usage 'cli.py <command> <param>'")
        if self.param not in self.valid_params:
            raise ValueError(f"Invalid type choice '{self.param}'")
        type_choice: str = {
            "series": "Series",
            "movies": "Movies",
        }.get(self.param, "unknown")
        return type_choice

    def _is_supported_image(self, filename: str) -> bool:
        """
        Checks if a file has a supported image extension.
        """
        return any(
            filename.lower().endswith(
                ext,
            )
            for ext in self.supported_formats
        )
