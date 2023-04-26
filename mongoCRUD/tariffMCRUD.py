from bson import ObjectId

from models.engine import mongo_async_decorator


class MongoCRUDTariff(object):

    @staticmethod
    @mongo_async_decorator
    async def get(client, tariff_id: str):
        try:
            collection = client["chatbotSNG"]["tarifs"]

            tariff = await collection.find_one({'_id': ObjectId(tariff_id)})
            return tariff
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    @mongo_async_decorator
    async def get_all(client):
        try:
            data_users = []
            collection = client["chatbotSNG"]['tarifs']

            async for user in collection.find():
                data_users.append(
                    {
                        "id": user['_id'],
                        "Name": user['Name'],
                        "Days": user['Days'],
                        "Price": user['Price']
                    }
                )
            return data_users
        except Exception as e:
            print(f"Error executing query: {e}")
            return None