from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from typing import List

from app.config.connection_db import get_prisma
from app.dependencies.auth import get_current_user
from app.model.diary import CreatePokemonDiary, UpdatePokemonDiary, PokemonDiaryResponse
from app.schemas.generic import ResponseSchema
from app.services.diary import PokemonService
from app.services.pokemon_api import PokemonAPIService
from app.messaging.diary import publish_diary_created, publish_diary_updated, publish_diary_deleted
from app.services.users import UsersService


router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/diary", response_model=ResponseSchema)
async def create_diary(data: CreatePokemonDiary, prisma: Prisma = Depends(get_prisma),
    current_user=Depends(get_current_user)):
    """
    Create a new Pokemon diary entry for the logged user.
    """
    user = await UsersService.get_user_by_id(prisma, current_user["id"])

    diary = await PokemonService.create_diary(prisma, current_user["id"], data)

    await publish_diary_created(current_user["id"], user.name)

    return ResponseSchema(
        detail="Pokemon diary created successfully",
        result=PokemonDiaryResponse.model_validate(diary)
    )


@router.get("/diary", response_model=ResponseSchema[List[PokemonDiaryResponse]])
async def get_user_diary(prisma: Prisma = Depends(get_prisma), current_user=Depends(get_current_user)):
    """
    Get all Pokemon diary entries for the logged user.
    """
    diaries = await PokemonService.get_user_diary(prisma, current_user["id"])

    if not diaries:
        raise HTTPException(
            status_code=404,
            detail="Diaries not found"
        )

    return ResponseSchema[List[PokemonDiaryResponse]](
        detail="Successfully fetched pokemon diary",
        result=[PokemonDiaryResponse.model_validate(d) for d in diaries]
    )


@router.patch("/diary/{diary_id}", response_model=ResponseSchema)
async def update_diary(diary_id: int, update_form: UpdatePokemonDiary, prisma: Prisma = Depends(get_prisma),
                       current_user=Depends(get_current_user)):
    """
    Update a Pokemon diary entry.
    Only the owner can update.
    """
    diary = await PokemonService.get_diary_by_id(prisma, diary_id)

    if not diary:
        raise HTTPException(
            status_code=404,
            detail="Diary not found"
        )

    if diary.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    updated_diary = await PokemonService.update_diary(prisma, diary_id, update_form)

    updated_fields = update_form.model_dump(exclude_unset=True)

    await publish_diary_updated(current_user["id"], updated_fields)

    return ResponseSchema(
        detail="Pokemon diary updated successfully",
        result=PokemonDiaryResponse.model_validate(updated_diary)
    )


@router.delete("/diary/{diary_id}", response_model=ResponseSchema)
async def delete_diary(diary_id: int, prisma: Prisma = Depends(get_prisma), current_user=Depends(get_current_user)):
    """
    Delete a Pokemon diary entry.
    Owner can delete their own diary, admin can delete any diary.
    """
    diary = await PokemonService.get_diary_by_id(prisma, diary_id)

    if not diary:
        raise HTTPException(
            status_code=404,
            detail="Diary not found"
        )

    is_owner = diary.user_id == current_user["id"]
    is_admin = current_user.get("role") == "admin"

    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    await publish_diary_deleted(current_user["id"], diary_id)

    await PokemonService.delete_diary(prisma, diary_id)

    return ResponseSchema(
        detail="Pokemon diary deleted successfully"
    )

@router.get("/search/{name}", response_model=ResponseSchema)
async def search_pokemon(name: str):
    """
    Search Pokemon data from external API (PokeAPI).
    """
    data = PokemonAPIService.get_pokemon(name)

    return ResponseSchema(
        detail="Pokemon fetched successfully",
        result=data
    )