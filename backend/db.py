from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import settings


engine = create_async_engine(
    settings.DATABASE_URL, 
    echo = True
)

async_session = sessionmaker(
    engine, 
    class_ = AsyncSession, 
    expire_on_commit = False
)

Base = declarative_base()

async def get_db():
    async with async_session() as db:
        yield db

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
