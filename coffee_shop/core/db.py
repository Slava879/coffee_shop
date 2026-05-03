from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Base(DeclarativeBase, AsyncAttrs): ...


class DatabaseManager:
    def __init__(self, db_url: str):
        self.__db_url = db_url

    async def __aenter__(self):
        self.__engine = create_async_engine(self.__db_url)
        self.__session_maker = async_sessionmaker(
            self.__engine, autoflush=False, expire_on_commit=False
        )

        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def __aexit__(self, exc_type, exc, tb):
        await self.__engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        async with self.__session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


async def get_session(request: Request):
    db_manager: DatabaseManager = request.app.state.db_manager
    async with db_manager.get_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]