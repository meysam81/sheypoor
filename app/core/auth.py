from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.jwt import ExpiredSignatureError
from passlib.context import CryptContext

from app.core.config import config, db_config
from app.db.v1.db import db
from app.models.v1.auth import TokenData, UserInDB

SECRET_KEY = config.JWT_SECRET
ALGORITHM = config.JWT_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    user = await db.read_one(username=username, table=db_config.USERS_COLLECTION_NAME)
    if user:
        return UserInDB(**user)

    # TODO: remove this in production
    return UserInDB(
        **{
            "username": "meysam",
            "hashed_password": "$2b$12$ARvhYuySXdEZ5e4PyOv5.OuVvc619o85ISaaqCVr1.d/MbnM2XBHy",
            "phone_number": "+989197050256",
        },
    )


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_():
    pass
