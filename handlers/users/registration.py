from aiogram import types

from loader import dp
from models import create_sync_session


async def addUser(collection):
    a = []
    async for document in collection.find({'date': {'$lt': "2024-04-17"}}):
        a.append(document)
        print(document)
    pass
    return a
a = "app:IPna2eocn9a1XqNEVrbL@'localhost:27017/chatbotSNG?authSource=admin)"

@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    await message.answer(text="Привет!")
    client = create_sync_session()
    a = await addUser(collection=client)
    await message.answer(text=str(a))
    print(a)
    pass
