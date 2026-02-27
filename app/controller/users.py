from fastapi import APIRouter, Depends
from prisma import Prisma
from typing import List

from app.config.connection_db import get_prisma
from app.model.users import CreateUser, UpdateUser, UserResponse
from app.schemas.users import ResponseUsersSchema
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=ResponseUsersSchema[List[UserResponse]])
async def get_all_users(prisma: Prisma = Depends(get_prisma)):
    users = await UsersService.get_all_users(prisma)

    return ResponseUsersSchema[List[UserResponse]](
        detail="Successfully fetched users",
        result=[UserResponse.model_validate(u) for u in users]
    )

@router.get("/{user_id}", response_model=ResponseUsersSchema)
async def get_user_by_id(user_id: int, prisma: Prisma = Depends(get_prisma)):
    user = await UsersService.get_user_by_id(prisma, user_id)

    return ResponseUsersSchema(
        detail="Successfully fetched user",
        result=UserResponse.model_validate(user)
    )

@router.post("", response_model=ResponseUsersSchema)
async def create_user(data: CreateUser, prisma: Prisma = Depends(get_prisma)):
    created_user = await UsersService.create_user(prisma, data)

    return ResponseUsersSchema(
        detail="User created successfully",
        result=UserResponse.model_validate(created_user)
    )

@router.patch("/{user_id}", response_model=ResponseUsersSchema)
async def update_user(user_id: int, update_form: UpdateUser, prisma: Prisma = Depends(get_prisma)):
    updated_user = await UsersService.update_user(prisma, user_id, update_form)

    return ResponseUsersSchema(
        detail="User updated successfully",
        result=UserResponse.model_validate(updated_user)
    )

@router.delete("/{user_id}", response_model=ResponseUsersSchema)
async def delete_user(user_id: int, prisma: Prisma = Depends(get_prisma)):
    await UsersService.delete_user(prisma, user_id)

    return ResponseUsersSchema(
        detail="User deleted successfully"
    )