from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import CONFIG

from motor.motor_asyncio import AsyncIOMotorClient
import motor

cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

SYNC_ENGINE = create_engine(f"postgresql://{CONFIG.DATABASE.POSTGRES}")
ASYNC_ENGINE = create_async_engine(f"postgresql+asyncpg://{CONFIG.DATABASE.POSTGRES}")
Session = sessionmaker(bind=SYNC_ENGINE)


def create_sync_session(func):
    def wrapper(**kwargs):
        with Session() as session:
            return func(**kwargs, session=session)
    return wrapper


def create_async_session(func):
    async def wrapper(**kwargs):
        async with AsyncSession(bind=ASYNC_ENGINE) as session:
            return await func(**kwargs, session=session)
    return wrapper


async def create_mongo_session():
    client = cluster.chatbotSNG
    return client

