import sys
import logging

from core.settings.config import Config
from core.interfaces.command_interface import ICommand
from core.manager.command_factory import CommandFactory
from core.utils.exceptions import PathNotFound, CommandNotFound
from core.utils.logging import setup_logging

setup_logging()


def main() -> None:
    try:
        cf = Config()
        if len(sys.argv) < 2:
            raise CommandNotFound("Usage 'cli.py <command>'")
        command_name: str = sys.argv[1]
        param: str = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
        command: ICommand = CommandFactory.get_command(cf, command_name, param)
        command.execute()
    except ValueError as e:
        logging.error(f"[Value]: {e}")
    except PathNotFound as e:
        logging.error(f"[Path]: {e}")
    except FileNotFoundError as e:
        logging.error(f"[File]: {e}")
    except CommandNotFound as e:
        logging.error(f"[Command]: {e}")
    except Exception as e:
        logging.error(f"[Unexpected]: {e}")


if __name__ == "__main__":
    main()
