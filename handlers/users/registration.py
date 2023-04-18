import datetime

from aiogram import types

from loader import dp
from models import create_sync_session


async def get_name(coll):
    a = await coll.find_one({"name": "vlad"})
    return a


async def get_date(collection):
    a = []
    async for document in collection.find():
        fariffEnd = datetime.datetime.strptime(document['TariffEnd'], '%Y-%m-%d %H:%M:%S.%f').date()
        if fariffEnd < datetime.datetime.now().date():
            a.append(document)
        print(document)
    return a


async def get_tariff(col) -> list:
    data = []
    collection = col.tarifs
    async for tariff in collection.find():
        data.append({"Name": tariff['Name'], "Price": tariff['Price'], "Days": tariff['Days']})
    return data


async def get_users(col) -> list:
    users_data = []
    collection = col.users
    async for user in collection.find():
        users_data.append({"Name": user['Name'],
                           "Email": user['Email'],
                           "TariffEnd": user['TariffEnd'],
                           "Money": user['Money'],
                           "NameTariff": user['NameTariff']
                           })
    return users_data


@dp.message_handler(commands=["tariff"])
async def tariff(message: types.Message):
    await message.answer(text="Доступные тарифы")
    client = create_sync_session()
    a = await get_tariff(col=client)
    text = ""
    for i in a:
        text += f"Название тарифа: {i['Name']}\n" \
                f"Цена - {i['Price']}\n" \
                f"Дней использования - {i['Days']}\n\n"

    await message.answer(text=text)


@dp.message_handler(commands=["users"])
async def g_users(message: types.Message):
    await message.answer(text="Пользователи")

    client = create_sync_session()
    a = await get_users(col=client)
    text = ""
    for i in a:
        text += f"Имя: {i['Name']}\n" \
                f"Email - {i['Email']}\n" \
                f"Конец подписки - {i['TariffEnd']}\n" \
                f"Денег - {i['Money']}\n" \
                f"Тариф - {i['NameTariff']}\n\n"

    await message.answer(text=text)


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    await message.answer(text="Привет!")
    client = create_sync_session()
    a = await get_date(collection=client)

    await message.answer(text=str(a))
    print(a)
    pass
