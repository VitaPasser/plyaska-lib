from typing import Protocol


class SettingsLoggable(Protocol):
    logging_dir_path: str