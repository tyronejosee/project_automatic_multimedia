import os
import logging

from PIL import Image

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class ResizePostersCommand(ICommand):
    def __init__(
        self,
        param: str,
        directory: str,
    ) -> None:
        self.param: str = param
        self.directory: str = directory

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        file_paths: list[str] = self._find_files()
        if not file_paths:
            raise FileNotFoundError("No files found.")

        for file_path in file_paths:
            self._process_image(file_path)
        logging.info("Task completed successfully. 🎉")

    def _find_files(self) -> list[str]:
        """
        Finds files in the directory.
        """
        files: list[str] = []
        valid_extensions: set[str] = {".jpg", ".webp", ".png"}

        for root, _, archives in os.walk(self.directory):
            for archive in archives:
                if any(archive.endswith(ext) for ext in valid_extensions):
                    files.append(os.path.join(root, archive))
        return files

    def _process_image(self, file_path: str) -> None:
        """
        Processes the given image file.
        """
        try:
            with Image.open(file_path) as img:
                img_width, img_height = img.size

                if self.param == "series":
                    target_width, target_height = 909, 1280
                elif self.param == "movies":
                    target_width, target_height = 909, 1409
                else:
                    raise ValueError(f"Invalid type choice '{self.param}'")

                if (img_width, img_height) == (target_width, target_height):
                    logging.error("Image is already the correct size.")
                    return

                if img_width < target_width or img_height < target_height:
                    logging.error(f"Image {file_path} is too small.")
                    return

                img_aspect_ratio: float = img_width / img_height
                target_aspect_ratio: float = target_width / target_height

                if img_aspect_ratio > target_aspect_ratio:
                    # If the image is wider, crop the sides
                    new_width = int(img_height * target_aspect_ratio)
                    left = int((img_width - new_width) / 2)
                    right = int((img_width + new_width) / 2)
                    top = 0
                    bottom: int = img_height
                else:
                    # If the image is taller, crop the top and bottom
                    new_height = int(img_width / target_aspect_ratio)
                    top = int((img_height - new_height) / 2)
                    bottom = int((img_height + new_height) / 2)
                    left = 0
                    right = img_width

                # Perform the crop to match the target aspect ratio
                img_cropped: Image.Image = img.crop((left, top, right, bottom))

                img_resized: Image.Image = img_cropped.resize(
                    (target_width, target_height),
                    Image.Resampling.LANCZOS,
                )

                file_dir: str = os.path.dirname(file_path)
                new_file_path: str = os.path.join(file_dir, "cv.jpg")
                img_resized.convert("RGB").save(
                    new_file_path,
                    "JPEG",
                    quality=100,
                    dpi=(600, 600),
                )
                logging.info(f"Image saved as {new_file_path}")

        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
