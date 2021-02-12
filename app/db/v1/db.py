from app.core.config import db_config

from .base import BaseDB
from .mongodb import MongoDB

db: BaseDB = MongoDB(
    db_config.URI,
    db_config.DATABASE_NAME,
    db_config.CONNECTION_TIMEOUT,
    db_config.MIN_POOL_SIZE,
    db_config.MAX_POOL_SIZE,
)


__all__ = ("db",)
