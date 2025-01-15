from core.interfaces.config_interface import IConfig
from core.interfaces.command_interface import ICommand
from core.utils.exceptions import CommandNotFound
from core.commands.build_icons import BuildIconsCommand
from core.commands.copy_covers import CopyCoversCommand
from core.commands.extract_subtitles import ExtractSubtitlesCommand
from core.commands.set_folder_icons import SetFolderIcons
from core.commands.generate_anime_folders import GenerateAnimeFoldersCommand


class CommandFactory:
    @staticmethod
    def get_command(cf: IConfig, name: str, param: str) -> ICommand:
        """
        Factory method to create command instances based on the name.
        """
        commands: dict[str, ICommand] = {
            "copy_covers": CopyCoversCommand(
                cf.DIRECTORY,
                cf.OUTPUT_FOLDER,
            ),
            "extract_subtitles": ExtractSubtitlesCommand(
                cf.DIRECTORY,
            ),
            "build_icons": BuildIconsCommand(
                param,
                cf.SERIES_SIZE,
                cf.MOVIES_SIZE,
                cf.INPUT_FOLDER,
                cf.TEMP_FOLDER,
                cf.OUTPUT_FOLDER,
                cf.DESIRED_WIDTH,
                cf.DESIRED_HEIGHT,
                cf.SUPPORTED_FORMATS,
            ),
            "set_folder_icons": SetFolderIcons(
                param,
                cf.INPUT_FOLDER,
                cf.ICON_FOLDER,
            ),
            "generate_folders": GenerateAnimeFoldersCommand(
                cf.DIRECTORY,
                cf.HEADERS_EN,
                cf.ELEMENTS_TO_SCRAPE,
                cf.ANIME_URL,
            ),
        }
        if name not in commands:
            raise CommandNotFound(f"Command '{name}' is not available.")
        return commands[name]
