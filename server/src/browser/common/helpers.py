from pathlib import Path


def get_root_directory_path() -> Path:
    return Path(__file__).parent.parent.parent.parent