from fastapi import APIRouter, Path
from app.schemas.users import ResponseUsersSchema
from app.services.users import UsersService
from app.model.users import CreateUser

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get("", response_model=ResponseUsersSchema, response_model_exclude_none=True)
async def get_all_users():
    result = await UsersService.get_all_users()
    return ResponseUsersSchema(detail="Successfully get all users!", result=result)


@router.get("/{id}", response_model=ResponseUsersSchema, response_model_exclude_none=True)
async def get_user_by_id(user_id: int = Path(..., alias="id")):
    result = await UsersService.get_user_by_id(user_id)
    return ResponseUsersSchema(detail="Successfully get user by id!", result=result)


@router.post("", response_model=ResponseUsersSchema, response_model_exclude_none=True)
async def create_user(create_data: CreateUser):
    await UsersService.create_user(create_data)
    return ResponseUsersSchema(detail="Successfully created user!")


@router.patch("/{id}", response_model=ResponseUsersSchema, response_model_exclude_none=True)
async def update_user(user_id: int = Path(..., alias="id"), *, update_form: CreateUser):
    await UsersService.update_user(user_id, update_form)
    return ResponseUsersSchema(detail="Successfully updated user!")


@router.delete("/{id}", response_model=ResponseUsersSchema, response_model_exclude_none=True)
async def delete_user(user_id: int):
    await UsersService.delete_user(user_id)
    return ResponseUsersSchema(detail="Successfully deleted user!")