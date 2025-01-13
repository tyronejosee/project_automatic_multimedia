from core.interfaces.command_interface import ICommand
from core.utils.exceptions import CommandNotFound


class CommandManager:
    def __init__(self) -> None:
        self.commands: dict[str, ICommand] = {}

    def register_command(self, name: str, command: ICommand) -> None:
        self.commands[name] = command

    def execute_command(self, name: str) -> None:
        if name in self.commands:
            self.commands[name].execute()
        else:
            raise CommandNotFound(f"Command '{name}' not found.")
