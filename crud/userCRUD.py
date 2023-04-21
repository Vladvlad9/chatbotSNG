from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserSchema, UserInDBSchema
from models import User, create_async_session


class CRUDUser(object):

    @staticmethod
    @create_async_session
    async def add(user: UserSchema, session: AsyncSession = None) -> UserInDBSchema:
        user = User(**user.dict())
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as eq:
            print(eq)
        else:
            await session.refresh(user)
            return UserInDBSchema(**user.__dict__)

    @staticmethod
    @create_async_session
    async def get(user_id: int, session: AsyncSession = None) -> UserInDBSchema:
        user = await session.execute(
            select(User)
            .where(User.user_id == user_id)
        )
        if user := user.first():
            return UserInDBSchema(**user[0].__dict__)
