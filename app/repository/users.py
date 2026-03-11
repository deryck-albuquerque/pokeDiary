from prisma import Prisma
from prisma.types import UsersCreateInput, UsersUpdateInput


class UsersRepository:

    @staticmethod
    async def get_all(prisma: Prisma):
        return await prisma.users.find_many()

    @staticmethod
    async def get_by_id(prisma: Prisma, user_id: int):
        return await prisma.users.find_unique(
            where={"id": user_id}
        )

    @staticmethod
    async def get_by_email(prisma: Prisma, email: str):
        return await prisma.users.find_unique(
            where={"email": email}
        )

    @staticmethod
    async def create(prisma: Prisma, data: UsersCreateInput):
        return await prisma.users.create(
            data=data
        )

    @staticmethod
    async def update(prisma: Prisma, user_id: int, data: UsersUpdateInput):
        return await prisma.users.update(
            where={"id": user_id},
            data=data
        )

    @staticmethod
    async def delete(prisma: Prisma, user_id: int):
        return await prisma.users.delete(
            where={"id": user_id}
        )