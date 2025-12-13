from typing import AsyncGenerator
from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    future=True,
    echo=False,
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]: #для работы с fast_api
    async with async_session() as session:
        yield session

SessionDep =  Annotated[AsyncSession, Depends(get_session)]

async def get_db_session() -> AsyncSession: #для работы вне fast_api
    async with async_session() as session:
        async with session.begin():
            yield session
