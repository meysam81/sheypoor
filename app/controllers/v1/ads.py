import asyncio
from uuid import UUID

from app.core.config import db_config
from app.db.v1.db import db
from app.models.v1.ads import AdDBRead, AdDBWrite, AdUpdateDB
from app.models.v1.auth import UserInDB
from app.schema.v1.ads import AdIn, AdOut, AdUpdate
from app.utils import exceptions
from app.utils.logger import logger

from .base import BaseController


class AdController(BaseController):
    async def create_new_ad(self, ad: AdIn, user: UserInDB) -> AdOut:
        try:
            ad_db_write = AdDBWrite(**ad.dict(), contact=user.phone_number)
            await db.insert_one(ad_db_write.dict(), table=db_config.ADS_COLLECTION_NAME)
            return ad_db_write

        except exceptions.BaseException_:
            raise

        except Exception:
            logger.exception("Traceback:")
            raise exceptions.ServerError

    async def get_all_ads(self, offset: int, limit: int):
        try:
            return await asyncio.gather(
                db.read_many(
                    table=db_config.ADS_COLLECTION_NAME, offset=offset, limit=limit
                ),
                db.count(table=db_config.ADS_COLLECTION_NAME),
            )

        except exceptions.BaseException_:
            raise

        except Exception:
            logger.exception("Traceback:")
            raise exceptions.ServerError

    async def get_an_ad(self, ad_id: UUID):
        try:
            ad = await db.read_one(table=db_config.ADS_COLLECTION_NAME, id=ad_id)
            if not ad:
                raise exceptions.NotFound
            return ad

        except exceptions.BaseException_:
            raise

        except Exception:
            logger.exception("Traceback:")
            raise exceptions.ServerError

    async def delete_an_ad(self, ad_id: UUID, user: UserInDB):
        try:
            # see if the ad is for the current user
            ad = await db.read_one(table=db_config.ADS_COLLECTION_NAME, id=ad_id)
            if not ad:
                raise exceptions.NotFound
            ad_db = AdDBRead(**ad)
            if ad_db.contact != user.phone_number:
                raise exceptions.NonOwnerAccessForbidden
            await db.delete_one(table=db_config.ADS_COLLECTION_NAME, id=ad_id)

        except exceptions.BaseException_:
            raise

        except Exception:
            logger.exception("Traceback:")
            raise exceptions.ServerError

    async def update_an_ad(self, ad_id: UUID, new_ad: AdUpdate, user: UserInDB):
        try:
            ad = await db.read_one(table=db_config.ADS_COLLECTION_NAME, id=ad_id)
            if not ad:
                raise exceptions.NotFound
            ad_db = AdDBRead(**ad)
            if ad_db.contact != user.phone_number:
                raise exceptions.NonOwnerAccessForbidden
            updated = AdUpdateDB(**new_ad.dict(exclude_none=True)).dict(
                exclude_none=True
            )
            return await db.update_one(
                table=db_config.ADS_COLLECTION_NAME,
                criteria={"id": ad_id},
                **updated,
            )

        except exceptions.BaseException_:
            raise

        except Exception:
            logger.exception("Traceback:")
            raise exceptions.ServerError


controller = AdController()
