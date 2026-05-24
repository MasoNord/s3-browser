from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LocalSQLLiteConnectionConfig:
    storage_path: str

    @property
    def connection_url(self) -> str:
        return "sqlite+aiosqlite:///" + self.storage_path