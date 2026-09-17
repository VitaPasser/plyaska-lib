from typing import Protocol

from pydantic_settings import BaseSettings


class SettingsLoggable(Protocol):
    logging_dir_path: str