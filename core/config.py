from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# /home/alex/Рабочий стол/Learni_app/Learni
BASE_DIR = Path(__file__).parent.parent

class LoggingSettings(BaseModel):
    path: Path = BASE_DIR / "logging_config.yaml"
    encoding: str = "utf-8"
    mode: str = "r"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "public.pem"
    algorithm: str = "RS256"
    expire_time: int = 20 # minutes


class ApiSettings(BaseModel):
    port: str
    host: str


class DatabaseSettings(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    max_overflow: int
    pool_size: int

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='/home/alex/Рабочий стол/Learni_app/Learni/.env', 
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore"
    )
    db: DatabaseSettings
    api: ApiSettings
    auth_jwt: AuthJWT = AuthJWT()
    log: LoggingSettings = LoggingSettings()

settings = Settings()
