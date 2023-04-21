from sqlalchemy import Column, Integer, BigInteger, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    email = Column(Text)
    password = Column(Text)