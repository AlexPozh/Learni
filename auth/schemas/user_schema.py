from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)
    
    email: EmailStr
    password: bytes

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr
    password: bytes
    