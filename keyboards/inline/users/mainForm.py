import datetime
from decimal import Decimal
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from config import CONFIG
from crud.userCRUD import CRUDUser
from loader import bot
from models.engine import create_mongo_session
from mongoCRUD.tariffMCRUD import MongoCRUDTariff
from mongoCRUD.userMCRUD import MongoCRUDUser

main_cb = CallbackData("main", "target", "action", "id", "editId")


class MainForms:
    @staticmethod
    async def back_ikb(target: str, action: str) -> InlineKeyboardMarkup:
        """
        Общая кнопка назад
        :param target: указать для CallbackData параметр для первого запроса
        :param action: указать для CallbackData параметр для первого под запроса
        :return: Возвращает клавиатуру
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="◀️ Назад", callback_data=main_cb.new(target, action, 0, 0))
                ]
            ]
        )

    @staticmethod
    async def open_site_kb() -> ReplyKeyboardMarkup:
        """
        Клавиатура для перехода на сайт
        :return: возвтращет клавиатуру с одной кнопкой
        """
        return ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Войти',
                                   web_app=WebAppInfo(url="https://transcendent-tanuki-81f3c0.netlify.app")
                                   )
                ]
            ]
        )

    @staticmethod
    async def get_profile() -> InlineKeyboardMarkup:
        """
        Клавиатура Главного меню
        :return: Возвращает клавитуру с двумя кнопками
        """
        data_main_menu = {
            "Профиль": {"target": "Profile", "action": "get_profile", "user_id": 0},
            "Тарифы": {"target": "Tariff", "action": "get_tariff", "user_id": 0}
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['user_id'], 0))
                ] for name_menu, target_menu in data_main_menu.items()
            ]
        )

    @staticmethod
    async def select_tariff_ikb(tariff_id) -> InlineKeyboardMarkup:
        """
        Клавиатура которая находиться в "Тарифах" в которой
        :param tariff_id:
        :return:
        """
        data_main_menu = {
            "Подключить": {
                "target": "Tariff", "action": "subscription_days", "tariff_id": tariff_id
            },
            "◀️ Назад": {"target": "Tariff", "action": "get_tariff", "tariff_id": tariff_id}
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['tariff_id'],
                                                                   0)
                                         )
                ] for name_menu, target_menu in data_main_menu.items()
            ]
        )

    @staticmethod
    async def get_tariff() -> InlineKeyboardMarkup:
        """
        Клавитура которая находитьс в "тарифах"  для вывода имеющихся в БД тарифы (сор. за тавтологию)
        :return: возвр. клавиатуру с тарифами
        """
        client = await create_mongo_session()

        data = {}
        collection = client.tarifs
        async for tariff in collection.find():
            data[tariff['Name']] = {"target": "Tariff", "action": "selectTariff", "tariff_id": tariff['_id']}
        data['Назад'] = {"target": "Profile", "action": "get_profile", "tariff_id": 0}

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['tariff_id'], 0))
                ] for name_menu, target_menu in data.items()
            ]
        )

    @staticmethod
    async def subscription_days_ikb(tariff_id: str):
        """
        Клавиатура для выбора дней подписки на тариф
        * days - (форма передачи данных) _пояснение что происходот_ '1_0'
            первый параметр (1) это id месяца, второй параметр (0) это процент который нужно передать в
            другую клавиатуру

        :param tariff_id: для хранения id тарифа
        :return: возвр. клавиатуру с выбором месяца
        """
        subscriptionDataOne = {
            "1 Месяц": {"target": "Tariff", "action": "activate_tariff", "tariff_id": tariff_id, "days": "1_0"},
            "3 М. (-3%)": {"target": "Tariff", "action": "activate_tariff", "tariff_id": tariff_id, "days": "3_3"}
        }
        subscriptionDataTwo = {
            "5 М. (-5%)": {"target": "Tariff", "action": "activate_tariff", "tariff_id": tariff_id, "days": "5_5"},
            "12 М. (-10%)": {"target": "Tariff", "action": "activate_tariff", "tariff_id": tariff_id, "days": "12_10"},
        }

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['tariff_id'],
                                                                   target_menu['days'])
                                         ) for name_menu, target_menu in subscriptionDataOne.items()
                ],
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['tariff_id'],
                                                                   target_menu['days'])
                                         ) for name_menu, target_menu in subscriptionDataTwo.items()
                ],
                [
                    InlineKeyboardButton(text="◀️ Назад", callback_data=main_cb.new("Tariff", "selectTariff", tariff_id,
                                                                                    0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def activate_tariff(tariff_name: str, price: int) -> InlineKeyboardMarkup:
        """
        Клавиатура
        :param tariff_name: Передача имени тарифа для дальнейшего вывода его
        :param price: цена выбранного тарифа выше
        :return: Клавиатуру с одной кнопкой
        """
        data_main_menu = {
            "Оплатить": {
                "target": "Tariff", "action": "pay", "price": price, "tariff_id": tariff_name
            }
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'],
                                                                   target_menu['action'],
                                                                   target_menu['price'],
                                                                   target_menu['tariff_id'])
                                         )
                ] for name_menu, target_menu in data_main_menu.items()
            ]
        )

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("main"):
                data = main_cb.parse(callback_data=callback.data)

                if data.get("target") == "MainForm":
                    if data.get("action") == "get_main_form":
                        await callback.message.edit_text(text="Главное меню",
                                                         reply_markup=await MainForms.get_profile())

                elif data.get("target") == "Profile":
                    # переписать код для даты!
                    if data.get("action") == "get_profile":
                        user = await CRUDUser.get(user_id=callback.from_user.id)
                        mongo_user = await MongoCRUDUser.get(email=user.email, password=user.password)

                        get_tariff = await MongoCRUDTariff.get(tariff_id=mongo_user['Tariff'])
                        current_date = datetime.datetime.today().date()
                        get_tariffEnd = str(mongo_user['TariffEnd']).split("-")

                        a = datetime.date(int(get_tariffEnd[0]), int(get_tariffEnd[1]), int(get_tariffEnd[2]))
                        daysLeft = a - current_date

                        dd = str(daysLeft)

                        text = f"Ваш тариф - <i>{get_tariff['Name']}</>\n" \
                               f"Тариф заканчивается  через {dd.split()[0]} дней - <i>{mongo_user['TariffEnd']}</i>\n" \
                               f"Баланс - <i>{mongo_user['Money']}</i>"

                        await callback.message.edit_text(text=f"Профиль\n\n{text}",
                                                         reply_markup=await MainForms.back_ikb(
                                                             target="MainForm",
                                                             action="get_main_form"),
                                                         parse_mode="HTML"
                                                         )

                elif data.get("target") == "Tariff":
                    if data.get("action") == "get_tariff":
                        await callback.message.edit_text(text="Выберите тариф",
                                                         reply_markup=await MainForms.get_tariff()
                                                         )

                    elif data.get("action") == "selectTariff":
                        tariff = await MongoCRUDTariff.get(tariff_id=data.get("id"))

                        await callback.message.edit_text(text=f"Название тарифа - {tariff['Name']}\n"
                                                              f"Дней использования - {tariff['Days']}\n"
                                                              f"Цена - {tariff['Price']}",
                                                         reply_markup=await MainForms.select_tariff_ikb(
                                                             tariff_id=data.get('id')
                                                         ))

                    elif data.get('action') == 'subscription_days':
                        await callback.message.edit_text(text="Выберите количество (М - месяц)\n"
                                                              "Скидка (-..%)",
                                                         reply_markup=await MainForms.subscription_days_ikb(
                                                             tariff_id=data.get('id'))
                                                         )

                    elif data.get('action') == 'activate_tariff':
                        data_days = data.get('editId').split("_")
                        days = data_days[0]
                        get_percent = int(data_days[1])

                        tariff = await MongoCRUDTariff.get(tariff_id=data.get('id'))
                        percent = int(tariff['Price']) / 100 * get_percent

                        price = round(Decimal(tariff['Price'] - Decimal(percent)), 2)
                        text = f"Вы собираетесь подключить тариф <i>{tariff['Name']}</i>\n" \
                               f"на {days} М.\n" \
                               f"Стоимость тарифа {tariff['Price']}\n\n" \
                               f"Стоимость со скидкой - {price} р."
                        await callback.message.edit_text(text=text,
                                                         reply_markup=await MainForms.activate_tariff(
                                                             tariff_name=tariff['Name'],
                                                             price=price),
                                                         parse_mode="HTML")

                    elif data.get("action") == "pay":
                        tariff_name = data.get("editId")
                        get_price = float(data.get("id"))
                        amount = int(get_price) * 100
                        price = types.LabeledPrice(label='Оплата товара!', amount=int(amount))
                        # await callback.message.delete()
                        await bot.send_invoice(chat_id=callback.message.chat.id,
                                               title=f"Подключение тарифа \n{tariff_name}\n",
                                               description=f"Подключение тарифа\n{tariff_name}",
                                               provider_token=CONFIG.PAYTOKEN,
                                               currency='RUB',
                                               is_flexible=False,
                                               prices=[price],
                                               need_email=True,
                                               need_name=True,
                                               start_parameter='time-machine-example',
                                               payload='some-invoice-payload-for-our-internal-use'
                                               )
                        pass

        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                pass