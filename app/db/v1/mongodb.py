from typing import Optional

import bson
import pymongo.errors
from motor import motor_asyncio
from pymongo import ReturnDocument

from app.utils import exceptions
from app.utils.logger import logger

from .base import BaseDB


class MongoDB(BaseDB):
    """This class is the concrete implementation of mongodb database."""

    def __init__(
        self,
        uri: str,
        dbname: str,
        connection_timeout: int,
        min_pool_size: int,
        max_pool_size: int,
    ):
        super().__init__()

        self._database = dbname
        self._db = motor_asyncio.AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=connection_timeout,
            minPoolSize=min_pool_size,
            maxPoolSize=max_pool_size,
        ).get_database(
            dbname,
            codec_options=bson.codec_options.CodecOptions(
                uuid_representation=bson.binary.UUID_SUBTYPE
            ),
        )

        logger.info(f"Database connection to: {dbname}")

    @property
    def dbname(self):
        return self._database

    async def count(self, *, table: str) -> int:
        logger.debug(f"Count -> {table}")
        return await self._db[table].estimated_document_count()

    async def insert_one(self, document: dict, *, table: str) -> str:
        logger.debug(f"Insert One: {document} -> {table}")

        try:
            return str((await self._db[table].insert_one(document)).inserted_id)

        except pymongo.errors.DuplicateKeyError as exp:
            duplicate_value = exp.details["keyValue"]
            raise exceptions.BaseException_(
                status_code=exceptions.DuplicateValue.status_code,
                detail=f"Duplicate Value: {duplicate_value}",
            )

    async def read_one(
        self,
        table: str,
        **criteria: dict,
    ) -> dict:
        logger.debug(f"Read One: {criteria} -> {table}")

        result = await self._db[table].find_one(filter=criteria)

        logger.debug(f"Read one result: {result}")

        return result

    async def update_one(
        self,
        *,
        table: str,
        criteria: dict,
        **new_values: dict,
    ) -> dict:
        try:
            update = {"$set": new_values}

            logger.debug(f"Update one: {criteria} to {update} -> {table}")

            result = await self._db[table].find_one_and_update(
                filter=criteria,
                update=update,
                return_document=ReturnDocument.AFTER,
            )

            logger.debug(f"Update one result: {result}")

            return result

        except pymongo.errors.DuplicateKeyError as exp:
            duplicate_value = exp.details["keyValue"]
            raise exceptions.BaseException_(
                status_code=exceptions.DuplicateValue.status_code,
                detail=f"Duplicate Value: {duplicate_value}",
            )

    async def delete_one(self, *, table: str, **criteria: dict) -> bool:
        logger.debug(f"Delete One: {criteria} -> {table}")

        result = await self._db[table].delete_one(filter=criteria)

        logger.debug(
            f"Delete one Result: {result.acknowledged} deleted: {result.deleted_count}"
        )

        return result.deleted_count == 1

    async def read_many(
        self,
        table: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **criteria,
    ) -> list[dict]:
        logger.debug(f"Read many: {criteria} -> {table}")

        params = {}
        if offset is not None:
            params.update({"skip": offset})

        if limit is not None:
            params.update({"limit": limit})

        result = [doc async for doc in self._db[table].find(criteria, **params)]

        logger.debug(f"Read many result: {result}")

        return result
