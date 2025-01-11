import os

from core.manager.command_manager import CommandManager
from core.commands.extract_subtitles import ExtractSubtitlesCommand


def main() -> None:
    command_manager = CommandManager()
    directory: str = "D:/Test"

    if not os.path.isdir(directory):
        print(f"El directorio '{directory}' no es válido.")
        return

    command = ExtractSubtitlesCommand(directory)
    command_manager.register_command("extract_subtitle", command)
    command_manager.execute_command("extract_subtitle")


if __name__ == "__main__":
    main()
