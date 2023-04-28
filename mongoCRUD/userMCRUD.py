from pymongo.errors import OperationFailure

from models.engine import mongo_async_decorator


class MongoCRUDUser(object):

    @staticmethod
    @mongo_async_decorator
    async def get(client, email: str = None, password: str = None, telegram_id: int = None):
        try:
            collection = client["chatbotSNG"]['users']
            if telegram_id:
                user = await collection.find_one({"TelegramId": telegram_id})
                return user
            else:
                user = await collection.find_one({"Email": email, "Password": password})
                return user
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    @mongo_async_decorator
    async def update(client, email: str, password: str, telegramId: str = None, money: int = None):
        try:
            collection = client["chatbotSNG"]['users']
            if money:
                user = await collection.update_one({"Email": email, "Password": password},
                                                   {'$set': {"Money": money}}
                                                   )
            else:
                user = await collection.update_one({"Email": email, "Password": password},
                                                   {'$set': {"TelegramId": telegramId}}

                                                   )

            return user.raw_result['updatedExisting']
        except OperationFailure as e:
            print(f"Error {e}")
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    @mongo_async_decorator
    async def get_all(client):
        try:
            data_users = []
            collection = client["chatbotSNG"]['users']

            async for user in collection.find():
                data_users.append(
                    {
                        "id": user["_id"],
                        "Name": user['Name'],
                        "Email": user['Email'],
                        "TariffEnd": user['TariffEnd'],
                        "Money": user['Money'],
                        "NameTariff": user['Tariff'],
                        "TelegramId": user['TelegramId']
                    }
                )
            return data_users
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
