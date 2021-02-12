from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(example="bearer")


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    phone_number: str
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class UserAuthenticate(BaseModel):
    username: str
    password: str
