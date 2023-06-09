import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from  config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# строка подключения к бд
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(DATABASE_URL)
# создание движка для работы с бд
# echo=True при инициализации движка позволит увидеть сгенерированные SQL-запросы в консоли
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session




