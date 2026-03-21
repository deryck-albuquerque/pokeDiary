import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma

from app.config.connection_db import get_prisma
from app.config.security import create_access_token
from app.model.users import LoginUser
from app.repository.users import UsersRepository
from app.messaging.auth import publish_user_login

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login(data: LoginUser, prisma: Prisma = Depends(get_prisma)):
    """
    Authenticate user and generate JWT token.
    """
    user = await UsersRepository.get_by_email(prisma, str(data.email))

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    password_valid = bcrypt.checkpw(data.password.encode(), user.password.encode())

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    await publish_user_login(user.id, user.email)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }