from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)
   
    email: EmailStr
    hash_password: str
    username: str | None = None


class LoginUser(BaseModel):
    model_config = ConfigDict(strict=True)

    email: str
    password: str


class CreateUserDB(CreateUser):
    hash_password: bytes
    is_email_confirmed: bool = False


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: str
    is_email_confirmed: bool
    registered_at: date


class NewPasswordScheme(BaseModel):
    email: str
    password: str


class NewPasswordDB(BaseModel):
    email: str
    hash_password: bytes