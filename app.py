import asyncio
from datetime import datetime

from aiogram.utils.exceptions import ChatNotFound

from keyboards.inline.users.mainForm import MainForms
from loader import bot
from mongoCRUD.userMCRUD import MongoCRUDUser
from utils.set_bot_commands import set_default_commands


async def scheduler():
    tasks = []
    while True:
        applicant_forms = list(filter(lambda x: x["TelegramId"] != "null", await MongoCRUDUser.get_all()))
        for user in applicant_forms:
            days_until_tariff = await MainForms.days_until_tariff_expiry(user["TariffEnd"])
            if days_until_tariff == 7:
                tasks.append(bot.send_message(chat_id=int(user['TelegramId']),
                                              text=f"До конца тарифа осталось 7 дней")
                             )
            elif days_until_tariff == 3:
                tasks.append(bot.send_message(chat_id=int(user['TelegramId']),
                                              text=f"До конца тарифа осталось 3 дня")
                             )
            elif days_until_tariff == 0:
                tasks.append(bot.send_message(chat_id=int(user['TelegramId']),
                                              text=f"До конца тарифа осталось 0 дней")
                             )
            await asyncio.gather(*tasks, return_exceptions=True)

            delay = datetime.now().date()
            delay = datetime(year=delay.year, month=delay.month, day=delay.day, hour=13) - datetime.now()
            delay = delay.seconds
            await asyncio.sleep(delay)


async def on_startup(_):
    await set_default_commands(dp)
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
