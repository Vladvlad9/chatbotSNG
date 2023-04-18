from config import CONFIG
from motor.motor_asyncio import AsyncIOMotorClient
import motor

cluster = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{CONFIG.DATABASE}")


def create_sync_session():
    client = cluster.chatbotSNG
    #collection = client.tarifs
    return client

