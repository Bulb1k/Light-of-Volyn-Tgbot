import aiosqlite
from typing import Optional
from data import config


class DB:
    database_name = config.DATABASE_NAME

    @classmethod
    async def insert(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            await db.execute(query, params)
            await db.commit()
            return True

    @classmethod
    async def select_one(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchone()

    @classmethod
    async def select_all(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchall()
