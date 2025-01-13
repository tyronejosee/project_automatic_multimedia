"""
Logging config.
"""

import logging

from colorlog import ColoredFormatter


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
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
