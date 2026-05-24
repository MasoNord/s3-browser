from dishka import Provider, Scope, provide

from browser.bootstrap.config.app import ApplicationConfig
from browser.bootstrap.config.sqlite import LocalSQLLiteConnectionConfig
from browser.infrastructure.config_loader import Config


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return Config.load_from_environment()

    @provide
    def local_db_connection(self, config: Config) -> LocalSQLLiteConnectionConfig:
        return config.db_connection


    @provide
    def app(self, config: Config) -> ApplicationConfig:
        return config.application_config

