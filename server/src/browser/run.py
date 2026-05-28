from dishka import Provider
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from browser.bootstrap.app_factory import create_web_app, create_ioc_container
from browser.bootstrap.config.logs import configure_logging, LoggingLevel
from browser.infrastructure.config_loader import Config
from browser.presentation.cors import setup_cors


def make_up(
    *di_providers: Provider,
) -> FastAPI:

    app_config = Config.load_from_environment()

    if app_config.application_config.logging_debug:
        configure_logging(LoggingLevel.DEBUG)
    else:
        configure_logging()

    app: FastAPI = create_web_app()

    container = create_ioc_container(*di_providers)

    setup_dishka(container, app)
    setup_cors(app)

    return app


app = make_up()