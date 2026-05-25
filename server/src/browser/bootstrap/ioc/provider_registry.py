from typing import Iterable

from dishka import Provider

from browser.bootstrap.ioc.application import ApplicationProvider
from browser.bootstrap.ioc.infrastructure import infrastructure_providers
from browser.bootstrap.ioc.settings import SettingsProvider


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        ApplicationProvider(),
        *infrastructure_providers()
    )
