from models.engine import create_mongo_session


class MongoCRUDUser(object):

    @staticmethod
    async def get(email: str, password: str) -> list:
        client = await create_mongo_session()
        collection = client.users
        user = await collection.find_one({"Email": email, "Password": password})
        return user