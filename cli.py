import sys
import logging

from core.interfaces.command_interface import ICommand
from core.manager.command_factory import CommandFactory
from core.settings.config import Config
from core.settings.database import Database
from core.utils.exceptions import PathNotFound, CommandNotFound
from core.utils.logging import setup_logging

setup_logging()


def main() -> None:
    try:
        cf = Config()
        database = Database()
        database.setup()

        # Parse arguments using argparse
        if len(sys.argv) < 2:
            raise CommandNotFound("Usage 'cli.py <command>'")
        command_name: str = sys.argv[1]
        param: str = sys.argv[2] if len(sys.argv) > 2 else "Unknown"

        # # Get command and execute
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
    finally:
        database.close()


if __name__ == "__main__":
    main()
