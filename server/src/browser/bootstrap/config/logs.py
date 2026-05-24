import datetime
import logging
from enum import StrEnum
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Final


# --- Настройки ---
class LoggingLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


DEFAULT_LOG_LEVEL: Final[LoggingLevel] = LoggingLevel.INFO
LOGS_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "logs"

FMT: Final[str] = (
    "[%(asctime)s.%(msecs)03d] "
    "[%(threadName)s] "
    "%(funcName)20s "
    "%(module)s:%(lineno)d "
    "%(levelname)-8s - "
    "%(message)s"
)
DATEFMT: Final[str] = "%Y-%m-%d %H:%M:%S"


class ExactLevelFilter(logging.Filter):
    def __init__(self, level: int):
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level

def create_timed_handler(level: int, logs_path: Path) -> logging.Handler:
    level_name = logging.getLevelName(level)
    level_dir = logs_path / level_name
    level_dir.mkdir(parents=True, exist_ok=True)

    current_date = datetime.date.today()

    file_path = level_dir / f"{current_date}.log"

    handler = TimedRotatingFileHandler(
        filename=file_path,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        utc=False,
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(FMT, DATEFMT))
    handler.addFilter(ExactLevelFilter(level))

    return handler


def configure_logging(level: LoggingLevel = DEFAULT_LOG_LEVEL) -> None:
    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(FMT, DATEFMT))
    root.addHandler(console_handler)

    for lvl in (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL):
        handler = create_timed_handler(lvl, LOGS_PATH)
        root.addHandler(handler)
