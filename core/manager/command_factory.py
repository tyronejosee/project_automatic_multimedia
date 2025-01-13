from core.interfaces.config_interface import IConfig
from core.interfaces.command_interface import ICommand
from core.utils.exceptions import CommandNotFound
from core.commands.copy_covers import CopyCoversCommand
from core.commands.extract_subtitles import ExtractSubtitlesCommand
from core.commands.generate_anime_folders import GenerateAnimeFoldersCommand


class CommandFactory:
    @staticmethod
    def get_command(name: str, cf: IConfig) -> ICommand:
        """
        Factory method to create command instances based on the name.
        """
        commands: dict[str, ICommand] = {
            "copy_covers": CopyCoversCommand(cf.DIRECTORY, cf.OUTPUT_FOLDER),
            "extract_subtitles": ExtractSubtitlesCommand(cf.DIRECTORY),
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
