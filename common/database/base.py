import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_async_engine(os.environ.get("DATABASE_URL"))
SessionMaker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
