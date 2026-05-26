from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class S3Bucket:
    name: str
    creation_date: datetime