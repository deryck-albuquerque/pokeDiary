import json
from fastapi import HTTPException
from app.model.pokemon import CreatePokemonDiary, UpdatePokemonDiary
from app.repository.pokemon import *

class PokemonService:

    @staticmethod
    async def create_diary(prisma: Prisma, user_id: int, data: CreatePokemonDiary) -> dict:
        """
        Creates diary in database.
        Validates that user doesn't already have a diary for this Pokemon.
        :param prisma: db connection
        :param user_id: int
        :param data: dict with field to create
        :return: dict
        """
        existing_diary = await PokemonRepository.get_by_user_and_pokemon_name(
            prisma, user_id, data.pokemon_name
        )

        if existing_diary:
            raise HTTPException(
                status_code=400,
                detail=f"You already have a diary for {data.pokemon_name}. Use update instead."
            )

        payload = {
            "pokemon_name": data.pokemon_name,
            "notes": json.dumps(data.notes) if data.notes else None,
            "user": {"connect": {"id": user_id}}
        }

        return await PokemonRepository.create(prisma, payload)

    @staticmethod
    async def get_user_diary(prisma: Prisma, user_id: int) -> dict:
        """
        Return a specific diary in database by user id.
        :param prisma: db connection
        :param user_id: int
        :return: dict
        """
        return await PokemonRepository.get_by_user(prisma, user_id)

    @staticmethod
    async def update_diary(prisma: Prisma, diary_id: int, data: UpdatePokemonDiary) -> dict:
        """
        Updates a specific diary by id.
        :param prisma: db connection
        :param diary_id: int
        :param data: dict with fields to update
        :return: dict
        """
        payload = {
            "pokemon_name": data.pokemon_name if data.notes else None,
            "notes": json.dumps(data.notes) if data.notes else None
        }

        return await PokemonRepository.update(prisma, diary_id, payload)

    @staticmethod
    async def delete_diary(prisma: Prisma, diary_id: int) -> dict:
        """
        Deletes a specific diary by id.
        :param prisma: db connection
        :param diary_id: int
        :return: dict
        """
        return await PokemonRepository.delete(prisma, diary_id)

    @staticmethod
    async def get_diary_by_id(prisma: Prisma, diary_id: int) -> dict:
        """
        Return a specific diary in database by user id.
        :param prisma: db connection
        :param diary_id: int
        :return: dict
        """
        return await PokemonRepository.get_by_id(prisma, diary_id)