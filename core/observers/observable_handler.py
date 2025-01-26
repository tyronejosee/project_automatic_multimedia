import sys
import logging
from logging import LogRecord

from core.utils.functions import remove_ansi_escape_codes
from .subject import ErrorLoggerSubject


class ObservableHandler(logging.StreamHandler):
    def __init__(self, subject: ErrorLoggerSubject) -> None:
        super().__init__(sys.stdout)
        self.subject: ErrorLoggerSubject = subject

    def emit(self, record: LogRecord) -> None:
        try:
            super().emit(record)

            if record.levelno >= logging.WARNING:
                log_entry: str = self.format(record)
                log_entry = remove_ansi_escape_codes(log_entry)
                self.subject.notify(log_entry)
        except Exception:
            self.handleError(record)
