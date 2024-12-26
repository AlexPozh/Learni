from datetime import timedelta, datetime, UTC

import jwt
import bcrypt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    alogrithm: str = settings.auth_jwt.algorithm
):
    new_fields_payload = payload.copy()
    new_fields_payload.update(
        iss="alex_learni_app",
        iat=int(datetime.now(UTC).timestamp()),
        exp=int((datetime.now(UTC) + timedelta(minutes=settings.auth_jwt.expire_time)).timestamp())
    )
    encoded = jwt.encode(
        new_fields_payload, 
        private_key, 
        alogrithm
    )
    return encoded


def decode_jwt(
    jwt_token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    alogrithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(
        jwt_token, 
        public_key, 
        algorithms=[alogrithm]
    )
    return decoded


def hash_password(
    password: str
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_pwd: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_pwd
    )