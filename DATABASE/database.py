from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from MODELS.M_fastapi_user import UserTable as Users

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine= create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        
async def get_user_db():
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, Users)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

# def get_user_db(session) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
#     yield SQLAlchemyUserDatabase(session, UserTable)
