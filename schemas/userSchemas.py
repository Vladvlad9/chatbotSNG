from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int
    email: str
    password: str


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
