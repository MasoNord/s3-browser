from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    host: str
    port: int
    logging_debug: bool = False