from dataclasses import dataclass
from datetime import datetime
from typing import List

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