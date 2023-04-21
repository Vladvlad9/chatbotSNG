from pydantic import BaseModel


class BotSchema(BaseModel):
    TOKEN: str
    ADMINS: list


class DateBaseSchema(BaseModel):
    MONGO: str
    POSTGRES: str


class ConfigSchema(BaseModel):
    BOT: BotSchema
    DATABASE: DateBaseSchema
    PAYTOKEN: str
