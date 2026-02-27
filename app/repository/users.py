from prisma import Prisma
from prisma.types import UsersCreateInput
from prisma.types import UsersUpdateInput

class UsersRepository:

    @staticmethod
    async def get_all_users(prisma: Prisma):
        return await prisma.users.find_many()

    @staticmethod
    async def get_user_by_id(prisma: Prisma, user_id: int):
        return await prisma.users.find_unique(
            where={"id": user_id}
        )

    @staticmethod
    async def create_user(prisma: Prisma, data: UsersCreateInput):
        return await prisma.users.create(
            data=data
        )

    @staticmethod
    async def update_user(prisma: Prisma, user_id: int, data: UsersUpdateInput):
        return await prisma.users.update(
            where={"id": user_id},
            data=data
        )

    @staticmethod
    async def delete_user(prisma: Prisma, user_id: int):
        return await prisma.users.delete(
            where={"id": user_id}
        )