from core.commands.build_icons import BuildIconsCommand
from core.commands.clean_files import CleanFilesCommand
from core.commands.resize_posters import ResizePostersCommand
from core.commands.copy_covers import CopyCoversCommand
from core.commands.data_loader import DataLoaderCommand
from core.commands.edit_mkv_metadata import EditMkvMetadataCommand
from core.commands.extract_media import ExtractMediaCommand
from core.commands.generate_anime_folders import GenerateAnimeFoldersCommand
from core.commands.generate_icon_folders import GenerateIconFoldersCommand
from core.commands.scan_disk import ScanDiskCommand
from core.commands.scan_library import ScanLibraryCommand
from core.commands.set_folder_icons import SetFolderIcons
from core.interfaces.command_interface import ICommand
from core.interfaces.config_interface import IConfig
from core.utils.exceptions import CommandNotFound
from .composite_command import CompositeCommand


class CommandFactory:
    @staticmethod
    def get_command(cf: IConfig, name: str, param: str) -> ICommand:
        """
        Factory method to create command instances based on the name.
        """
        commands: dict[str, ICommand] = {
            "build_icons": BuildIconsCommand(
                param,
                cf.SERIES_SIZE,
                cf.MOVIES_SIZE,
                cf.INPUT_FOLDER,
                cf.TEMP_FOLDER,
                cf.OUTPUT_FOLDER,
                cf.ICON_FOLDER,
                cf.DESIRED_WIDTH,
                cf.DESIRED_HEIGHT,
                cf.SUPPORTED_FORMATS,
            ),
            "generate_folders": GenerateAnimeFoldersCommand(
                cf.DIRECTORY,
                cf.HEADERS_EN,
                cf.ELEMENTS_TO_SCRAPE,
                cf.ANIME_URL,
            ),
            "set_folder_icons": SetFolderIcons(
                param,
                cf.DIRECTORY,
                cf.ICON_FOLDER,
            ),
            "data_loader": DataLoaderCommand(
                param,
                cf.ICON_FOLDER,
            ),
            "resize_posters": ResizePostersCommand(
                param,
                cf.DIRECTORY,
            ),
            "clean_files": CleanFilesCommand(
                cf.DIRECTORY,
                cf.CLEAN_FILES,
            ),
            "copy_covers": CopyCoversCommand(
                cf.DIRECTORY,
                cf.OUTPUT_FOLDER,
            ),
            "edit_mkv_metadata": EditMkvMetadataCommand(
                param,
                cf.DIRECTORY,
            ),
            "generate_type_folders": GenerateIconFoldersCommand(
                param,
                cf.ICON_FOLDER,
            ),
            "scan_disk": ScanDiskCommand(
                cf.DISK_PATHS,
            ),
            "scan_library": ScanLibraryCommand(
                cf.LIBRARY_PATHS,
            ),
            "extract_subtitles": ExtractMediaCommand(
                cf.DIRECTORY,
            ),
            # Composite Commands
            "build_folders": CompositeCommand(
                CopyCoversCommand(
                    cf.DIRECTORY,
                    cf.OUTPUT_FOLDER,
                ),
                BuildIconsCommand(
                    param,
                    cf.SERIES_SIZE,
                    cf.MOVIES_SIZE,
                    cf.INPUT_FOLDER,
                    cf.TEMP_FOLDER,
                    cf.OUTPUT_FOLDER,
                    cf.ICON_FOLDER,
                    cf.DESIRED_WIDTH,
                    cf.DESIRED_HEIGHT,
                    cf.SUPPORTED_FORMATS,
                ),
                SetFolderIcons(
                    param,
                    cf.DIRECTORY,
                    cf.ICON_FOLDER,
                ),
            ),
            "generate_folders_with_icon": CompositeCommand(
                GenerateIconFoldersCommand(
                    param,
                    cf.INPUT_FOLDER,
                ),
                SetFolderIcons(
                    param,
                    cf.INPUT_FOLDER,
                    cf.ICON_FOLDER,
                ),
            ),
        }
        if name not in commands:
            raise CommandNotFound(f"Command '{name}' is not available.")
        return commands[name]
