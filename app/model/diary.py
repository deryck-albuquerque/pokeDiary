from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class CreatePokemonDiary(BaseModel):
    pokemon_name: str
    notes: Optional[Dict[str, Any]] = None


class UpdatePokemonDiary(BaseModel):
    pokemon_name: Optional[str] = None
    notes: Optional[Dict[str, Any]] = None


class PokemonDiaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pokemon_name: str
    notes: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True