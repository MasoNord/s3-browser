import logging
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from browser.bootstrap.config.app import ApplicationConfig
from browser.bootstrap.config.sqlite import LocalSQLLiteConnectionConfig
from browser.common.helpers import get_root_directory_path

logger = logging.getLogger(__name__)

def to_bool(value: str) -> bool:
    return value.lower() in ("1", "true")

@dataclass
class Config:
    db_connection: LocalSQLLiteConnectionConfig
    application_config: ApplicationConfig

    @classmethod
    def load_from_environment(cls: type["Config"]) -> "Config":

        db = cls._load_db_config()

        application_config = ApplicationConfig(
            host=os.environ["APP_HOST"],
            port=int(os.environ["APP_PORT"]),
            logging_debug=to_bool(os.environ["APP_LOGGING_DEBUG"])
        )

        logger.debug("Config loaded.")

        return cls(
            db_connection=db,
            application_config=application_config
        )

    @classmethod
    def _load_db_config(cls: type["Config"]) -> LocalSQLLiteConnectionConfig:
        # Storage path
        if "DB_STORAGE_PATH" not in os.environ:
            storage_path = Path(get_root_directory_path()) / "storage"
        else:
            storage_path = Path(os.environ["DB_STORAGE_PATH"])

        storage_path.mkdir(parents=True, exist_ok=True)

        # Database path
        db_path = storage_path / "data.db"

        # Check if db is new
        is_new_database = not db_path.exists()

        # Create empty db file
        db_path.touch(exist_ok=True)

        # Bootstrap database
        if is_new_database:
            logger.debug("Initializing SQLite database...")

            init_sql_path = (
                Path(get_root_directory_path())
                / "src"
                / "browser"
                / "infrastructure"
                / "persistence"
                / "bootstrap"
                / "init.sql"
            )

            with open(init_sql_path, "r", encoding="utf-8") as f:
                init_sql = f.read()

            connection = sqlite3.connect(db_path)

            try:
                connection.executescript(init_sql)
                connection.commit()

                logger.debug("Database initialized.")

            finally:
                connection.close()

        return LocalSQLLiteConnectionConfig(
            storage_path=str(db_path)
        )

