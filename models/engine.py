from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import CONFIG

from motor.motor_asyncio import AsyncIOMotorClient
import motor

# cluster = AsyncIOMotorClient("mongodb://localhost:27017")
# client = AsyncIOMotorClient("mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority")
# "mongodb://app:IPna2eocn9a1XqNEVrbL@localhost:27017/chatbotSNG?authSource=admin
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


async def connect_to_mongo():
    """
    This function connects to a MongoDB database and returns the client object.
    """
    try:
        # Replace the connection string with your own MongoDB connection string
        client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG.DATABASE.MONGO)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def mongo_async_decorator(func):
    """
    This decorator function connects to a MongoDB database and passes the client object to the decorated function.
    """
    async def wrapper(**kwargs):
        client = await connect_to_mongo()
        if client:
            try:
                result = await func(client, **kwargs)
                return result
            except Exception as e:
                print(f"Error executing function: {e}")
                return None
        else:
            return None

    return wrapper
