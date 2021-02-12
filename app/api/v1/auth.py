from datetime import timedelta

from fastapi import APIRouter, Body, HTTPException, status

from app.core.auth import authenticate_user, create_access_token
from app.core.config import config
from app.models.v1.auth import Token, UserAuthenticate

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = config.JWT_EXPIRY


@router.post("/token", response_model=Token)
async def login_for_access_token(user_auth: UserAuthenticate = Body(...)):
    user = await authenticate_user(user_auth.username, user_auth.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
