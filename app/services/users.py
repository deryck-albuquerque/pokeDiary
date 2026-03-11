from prisma import Prisma
from app.model.users import CreateUser, UpdateUser, UserResponse
from app.repository.users import UsersRepository, UsersUpdateInput
import bcrypt


class UsersService:

    @staticmethod
    async def get_all_users(prisma: Prisma) -> dict:
        """
        Return all registered users in database.
        :param prisma: db connection
        :return: dict
        """
        return await UsersRepository.get_all(prisma)

    @staticmethod
    async def get_user_by_id(prisma: Prisma, user_id: int) -> dict:
        """
        Return a specific user in database by id.
        :param prisma: db connection
        :param user_id: int
        :return: dict
        """
        return await UsersRepository.get_by_id(prisma, user_id)

    @staticmethod
    async def create_user(prisma: Prisma, data: CreateUser) -> dict:
        """
        Creates user in database with name, email and password.
        :param prisma: db connection
        :param data: payload
        :return: dict
        """
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

        payload = data.model_dump()
        payload["password"] = hashed_password

        return await UsersRepository.create(prisma, payload)

    @staticmethod
    async def update_user(prisma: Prisma, user_id: int, data: UpdateUser) -> dict:
        """
        Updates a specific user by id.
        :param prisma: db connection
        :param user_id: int
        :param data: payload
        :return: dict
        """
        payload: UsersUpdateInput = data.model_dump(exclude_unset=True)

        return await UsersRepository.update(prisma, user_id, payload)

    @staticmethod
    async def delete_user(prisma: Prisma, user_id: int) -> dict:
        """
        Deletes a specific user by id.
        :param prisma: db connection
        :param user_id: int
        :return: dict
        """
        return await UsersRepository.delete(prisma, user_id)
