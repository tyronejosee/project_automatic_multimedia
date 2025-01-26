import logging

from colorlog import ColoredFormatter

from core.settings.config import Config as cf
from core.observers.observable_handler import ObservableHandler
from core.observers.discord_notifier import DiscordNotifier
from core.observers.subject import ErrorLoggerSubject


def setup_logging() -> None:

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    # Observer pattern
    error_subject = ErrorLoggerSubject()
    discord_notifier = DiscordNotifier(cf.DISCORD_URL)
    error_subject.attach(discord_notifier)
    handler = ObservableHandler(error_subject)
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
