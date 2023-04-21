from bson import ObjectId

from models.engine import create_mongo_session


class MongoCRUDTariff(object):

    @staticmethod
    async def get(tariff_id: str) -> list:
        client = await create_mongo_session()
        collection = client.tarifs
        tariff = await collection.find_one({'_id': ObjectId(tariff_id)})
        return tariff

    @staticmethod
    async def get_all():
        client = await create_mongo_session()
        collection = client.tarifs