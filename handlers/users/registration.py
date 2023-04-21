import datetime
import json

import aiogram.types
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from crud.userCRUD import CRUDUser
from keyboards.inline.users.mainForm import main_cb, MainForms
from loader import dp, bot
from bson.objectid import ObjectId

from models.engine import create_mongo_session
from mongoCRUD.tariffMCRUD import MongoCRUDTariff
from mongoCRUD.userMCRUD import MongoCRUDUser
from schemas import UserSchema
from states.users.userState import UserStates


#tariffEnd = datetime.datetime.strptime(document['TariffEnd'], '%Y-%m-%d %H:%M:%S.%f').date()
async def get_name(coll):
    a = await coll.find_one({"name": "vlad"})
    return a


async def get_date(collection):
    a = []
    async for document in collection.find():
        tariffEnd = datetime.datetime.strptime(document['TariffEnd'], '%Y-%m-%d %H:%M:%S.%f').date()
        if tariffEnd < datetime.datetime.now().date():
            a.append(document)
        print(document)
    return a




async def get_current_tariff(col, tariff_id):
    collection = col.tarifs
    tariff = await collection.find_one({'_id': ObjectId(tariff_id)})
    return tariff


async def get_current_users(col, email, password) -> list:
    collection = col.users
    user = await collection.find_one({"Email": email, "Password": password})
    return user


@dp.message_handler(commands=["tariff"])
async def tariff(message: types.Message):
    await message.answer(text="Доступные тарифы")
    client = await create_mongo_session()
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

    client = await create_mongo_session()
    a = await get_users(col=client)
    text = ""
    for i in a:
        text += f"Имя: {i['Name']}\n" \
                f"Email - {i['Email']}\n" \
                f"Конец подписки - {i['TariffEnd']}\n" \
                f"Денег - {i['Money']}\n" \
                f"Тариф - {i['Tariff']}\n\n"

    await message.answer(text=text)


@dp.callback_query_handler(main_cb.filter())
@dp.callback_query_handler(main_cb.filter(), state=UserStates.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    get_user = await CRUDUser.get(user_id=message.from_user.id)
    if get_user:
        await message.answer(text="Главное меню",
                             reply_markup=await MainForms.get_profile())
    else:
        await message.answer(text="Добро пожаловать в Bot Kits"
                                  "Что бы авторизоваться в системе нужно пройти аутентификацию",
                             reply_markup=await MainForms.open_site_kb())


@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    get_data = json.loads(message.web_app_data.data)

    if get_data:
        user = await MongoCRUDUser.get(email=get_data['email'], password=get_data['password'])

        if user:
            await CRUDUser.add(user=UserSchema(user_id=message.from_user.id,
                                               **get_data)
                               )

            get_tariff = await MongoCRUDTariff.get(tariff_id=user['Tariff'])

            await message.answer(text=f"Вы успешно авторизовались {user['Name']}",
                                 reply_markup=aiogram.types.ReplyKeyboardRemove())

            await message.answer(text=f"Ваш тариф - {get_tariff['Name']}\n"
                                      f"Тариф заканчивается - {user['TariffEnd']}\n"
                                      f"Баланс - {user['Money']}",
                                 reply_markup=await MainForms.get_profile())
        else:
            await message.answer(text="Данного пользователя не существует")
    else:
        await message.answer(text="Неудалось получить данные с сайта авторизации")


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    try:
        await message.answer(text=f"Оплата прошла успешна!\n",
                             reply_markup=await MainForms.get_profile())
    except Exception as e:
        print(e)
        await message.answer(text=f"Оплата не прошла!\n",
                             reply_markup=await MainForms.get_profile())


