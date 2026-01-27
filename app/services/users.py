from app.model.users import CreateUser
from app.repository.users import UsersRepository

class UsersService:

    @staticmethod
    async def get_all_users():
        return await UsersRepository.get_all_users()

    @staticmethod
    async def get_user_by_id(user_id: int):
        return await UsersRepository.get_user_by_id(user_id)

    @staticmethod
    async def create_user(data: CreateUser):
        return await UsersRepository.create_user(data)

    @staticmethod
    async def update_user(user_id: int, data: CreateUser):
        return await UsersRepository.update_user(user_id, data)

    @staticmethod
    async def delete_user(user_id: int):
        return await UsersRepository.delete_user(user_id)
