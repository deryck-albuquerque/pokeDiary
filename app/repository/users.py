from app.model.users import CreateUser
from app.config.connection_db import prisma_connection

class UsersRepository:

    @staticmethod
    async def get_all_users():
        return await prisma_connection.prisma.users.find_many()

    @staticmethod
    async def get_user_by_id(user_id: int):
        return await prisma_connection.prisma.users.find_first(where={"id": user_id})

    @staticmethod
    async def create_user(user: CreateUser):
        return await prisma_connection.prisma.users.create({
            "name": user.name,
            "email": user.email,
            "password": user.password
        })

    @staticmethod
    async def update_user(user_id: int, user: CreateUser):
        await prisma_connection.prisma.users.update(where={"id": user_id}, data={
            "name": user.name,
            "email": user.email,
            "password": user.password
        })

    @staticmethod
    async def delete_user(user_id: int):
        await prisma_connection.prisma.users.delete(user_id)
