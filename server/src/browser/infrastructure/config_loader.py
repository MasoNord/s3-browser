import logging
import os
from dataclasses import dataclass

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

        # Check if a user set a custom SQL Lite location
        stored_path = ""
        if "DB_STORAGE_PATH" not in  os.environ:
            stored_path = get_root_directory_path() / "storage"
        else:
            # TODO: add check if db storage path exists
            stored_path = os.environ["DB_STORAGE_PATH"]

        # Creat storage folder if not exists
        os.makedirs(stored_path, exist_ok=True)

        # Create .db file if not exists
        data_path = os.path.join(stored_path, "data.db")

        if not os.path.exists(data_path):
            with open(data_path, "w") as f:
                pass

        db = LocalSQLLiteConnectionConfig(
            storage_path=data_path
        )

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
