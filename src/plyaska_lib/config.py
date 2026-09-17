from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

from plyaska_lib.logging.settings_logging_protocol import SettingsLoggable

basepath = Path(__file__).parent.parent.parent


class Settings(BaseSettings, SettingsLoggable):
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    redis_host: str
    redis_port: int
    server_internal_port: int
    server_internal_host: str
    server_internal_host_domain: str
    server_internal_protocol: str
    server_external_port: int
    server_hot_reloaded_on: str
    server_count_workers: int
    logging_dir_path: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=basepath / ".env",
        case_sensitive=False,
        extra="ignore",
        env_file_encoding="utf-8",
    )

    def make_url(self):
        return f"{self.server_internal_protocol}://{self.server_internal_host_domain}:{str(self.server_internal_port)}"


settings = Settings()  # type: ignore
