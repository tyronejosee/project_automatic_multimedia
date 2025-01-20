from core.interfaces.command_interface import ICommand


class CompositeCommand(ICommand):
    def __init__(self, *commands: ICommand) -> None:
        self.commands: tuple[ICommand, ...] = commands

    def execute(self) -> None:
        for command in self.commands:
            command.execute()
