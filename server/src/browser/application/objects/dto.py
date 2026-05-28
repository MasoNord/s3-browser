from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class ObjectFile:
    name: str
    full_key: str
    size: int
    last_modified: datetime

@dataclass
class ObjectFolder:
    name: str
    full_key: str

@dataclass
class ReadObject:
    current_prefix: str
    folders: List[ObjectFolder]
    files: List[ObjectFile]

@dataclass
class UploadObject:
    filename: str
    bucket_name: str
    prefix: str | None
    file: bytes
    size: int
    content_type: str
    delimiter: str = "/"