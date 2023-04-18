from pydantic import BaseModel


class BotSchema(BaseModel):
    TOKEN: str
    ADMINS: list


class ConfigSchema(BaseModel):
    BOT: BotSchema
    DATABASE: str
