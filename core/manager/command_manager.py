from core.commands.command import Command


class CommandManager:
    def __init__(self) -> None:
        self.commands: dict[str, Command] = {}

    def register_command(self, name: str, command: Command) -> None:
        self.commands[name] = command

    def execute_command(self, name: str) -> None:
        if name in self.commands:
            self.commands[name].execute()
        else:
            print(f"Command '{name}' not found!")
