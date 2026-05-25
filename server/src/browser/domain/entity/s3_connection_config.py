from datetime import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class ConnectionConfig:
    id: UUID
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    created_at: datetime
    last_used_at: datetime