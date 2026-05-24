from dishka import Provider
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from browser.bootstrap.app_factory import create_web_app, create_ioc_container
from browser.bootstrap.config.logs import configure_logging, LoggingLevel
from browser.infrastructure.config_loader import Config


def make_up(
    *di_providers: Provider,
) -> FastAPI:

    # Set up Logging
    app_config = Config.load_from_environment()
    if app_config.application_config.logging_debug:
        configure_logging(LoggingLevel.DEBUG)
    else:
        configure_logging()

    # Create app
    app: FastAPI = create_web_app()

    # Set up IOC container
    container = create_ioc_container(*di_providers)
    setup_dishka(container, app)

    return app

def create_app():
    return make_up()

if __name__ ==  "__main__":
    import uvicorn

    config = Config.load_from_environment()

    uvicorn.run(
        app=make_up(),
        reload=True,
        host=config.application_config.host,
        port=config.application_config.port,
        reload_dirs=["src/"],
        reload_excludes=["*.log", "*.tmp", "__pycache__"],
    )