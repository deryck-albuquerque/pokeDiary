from prisma import Prisma

class PokemonRepository:

    @staticmethod
    async def create(prisma: Prisma, data: dict):
        return await prisma.pokemondiary.create(data=data)

    @staticmethod
    async def get_by_user(prisma: Prisma, user_id: int):
        return await prisma.pokemondiary.find_many(
            where={"user_id": user_id}
        )

    @staticmethod
    async def get_by_user_and_pokemon_name(prisma: Prisma, user_id: int, pokemon_name: str):
        return await prisma.pokemondiary.find_first(
            where={
                "user_id": user_id,
                "pokemon_name": pokemon_name
            }
        )

    @staticmethod
    async def update(prisma: Prisma, diary_id: int, data: dict):
        return await prisma.pokemondiary.update(
            where={"id": diary_id},
            data=data
        )

    @staticmethod
    async def delete(prisma: Prisma, diary_id: int):
        return await prisma.pokemondiary.delete(
            where={"id": diary_id}
        )

    @staticmethod
    async def get_by_id(prisma: Prisma, diary_id: int):
        return await prisma.pokemondiary.find_unique(
            where={"id": diary_id}
        )