from typing import Optional

from pydantic import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file: str = ".env"


class GlobalConfig(BaseSettings):
    ENV_STATE: Optional[str] = "dev"
    API_URI: str = "/api"
    LOG_LEVEL: str = "INFO"


class DevConfig(GlobalConfig):
    JWT_SECRET: str
    JWT_ALGORITHM: Optional[str] = "HS256"
    JWT_EXPIRY: Optional[int] = 7200  # 2 hours by default

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRY: int

    class Config:
        env_prefix: str = "PROD_"


class DBConfig(BaseSettings):
    URI: str
    DATABASE_NAME: str
    CONNECTION_TIMEOUT: int = 3000
    MIN_POOL_SIZE: int = 10
    MAX_POOL_SIZE: int = 50

    USERS_COLLECTION_NAME: str = "users"
    ADS_COLLECTION_NAME: str = "ads"

    class Config:
        env_prefix: str = "DB_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state.lower()

    def __call__(self):
        if self.env_state.startswith("dev"):
            return DevConfig()

        elif self.env_state.startswith("prod"):
            return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()
db_config = DBConfig()
