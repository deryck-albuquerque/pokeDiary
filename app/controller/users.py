from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from typing import List

from app.config.connection_db import get_prisma
from app.dependencies.auth import get_current_user, require_role
from app.model.users import CreateUser, UpdateUser, UserResponse
from app.schemas.users import ResponseUsersSchema
from app.services.users import UsersService
from app.core.roles import Role
from app.messaging.users import publish_user_created, publish_user_updated, publish_user_deleted

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("", response_model=ResponseUsersSchema[List[UserResponse]])
async def get_all_users(prisma: Prisma = Depends(get_prisma), current_user=Depends(require_role(Role.ADMIN))):
    """
    Admin only: return all users.
    """
    users = await UsersService.get_all_users(prisma)

    return ResponseUsersSchema[List[UserResponse]](
        detail="Successfully fetched users",
        result=[UserResponse.model_validate(u) for u in users]
    )


@router.get("/{user_id}", response_model=ResponseUsersSchema)
async def get_user_by_id(user_id: int, prisma: Prisma = Depends(get_prisma),
                         current_user: dict = Depends(get_current_user)):
    """
    User can access only their own profile.
    Admin can access any user.
    """
    if current_user["role"] != Role.ADMIN and current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    user = await UsersService.get_user_by_id(prisma, user_id)

    return ResponseUsersSchema(
        detail="Successfully fetched user",
        result=UserResponse.model_validate(user)
    )


@router.post("", response_model=ResponseUsersSchema)
async def create_user(data: CreateUser, prisma: Prisma = Depends(get_prisma)):
    """
    Public route: create a new user.
    """
    created_user = await UsersService.create_user(prisma, data)

    # messaging rabbitMQ
    await publish_user_created(created_user.name, created_user.email, created_user.role, created_user.id)

    return ResponseUsersSchema(
        detail="User created successfully",
        result=UserResponse.model_validate(created_user)
    )


@router.patch("/{user_id}", response_model=ResponseUsersSchema)
async def update_user(user_id: int, update_form: UpdateUser, prisma: Prisma = Depends(get_prisma),
                      current_user: dict = Depends(get_current_user)):
    """
    User can update their own account.
    Admin can update any account.
    """
    if current_user["role"] != Role.ADMIN and current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    updated_user = await UsersService.update_user(prisma, user_id, update_form)

    updated_fields = update_form.model_dump(exclude_unset=True)

    # messaging rabbitMQ
    await publish_user_updated(user_id, updated_fields)

    return ResponseUsersSchema(
        detail="User updated successfully",
        result=UserResponse.model_validate(updated_user)
    )


@router.delete("/{user_id}", response_model=ResponseUsersSchema)
async def delete_user(user_id: int, prisma: Prisma = Depends(get_prisma),
                      current_user=Depends(require_role(Role.ADMIN))):
    """
    Admin only: delete user.
    """
    user = await UsersService.get_user_by_id(prisma, user_id)

    await publish_user_deleted(user.name, user.email, user.role, user.id)

    await UsersService.delete_user(prisma, user_id)

    return ResponseUsersSchema(detail="User deleted successfully")