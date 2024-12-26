from datetime import date

from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)
   
    email: EmailStr
    hash_password: str
    username: str | None = None


class CreateUserDB(CreateUser):
    hash_password: bytes
    is_email_confirmed: bool = False

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr
    is_email_confirmed: bool
    registered_at: date