import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
SOURCE_DIR = Path(__file__).resolve().parent.parent


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    matches: str = "/matches"
    teams: str = "/teams"
    referees: str = "/referees"
    divisions: str = "/divisions"
    seasons: str = "/seasons"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class CorsConfig(BaseModel):
    allowed_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    test_url: PostgresDsn | None = None
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=SOURCE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging_config: LoggingConfig = LoggingConfig()
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()
    cors: CorsConfig = CorsConfig()


settings = Settings()
