import requests
import os
from fastapi import HTTPException


class PokemonAPIService:

    BASE_URL = os.getenv("POKEMON_API_URL")

    @staticmethod
    def get_pokemon(name: str) -> dict:
        """
        Fetch full Pokemon data including:
        - types
        - abilities
        - stats
        - moves (limited)
        - height/weight
        - description
        - evolutions
        """

        url = f"{PokemonAPIService.BASE_URL}/{name.lower()}"
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Pokemon not found"
            )

        data = response.json()

        types = [t["type"]["name"] for t in data["types"]]

        abilities = [a["ability"]["name"] for a in data["abilities"]]

        stats = {
            stat["stat"]["name"]: stat["base_stat"]
            for stat in data["stats"]
        }

        moves = [m["move"]["name"] for m in data["moves"][:5]]

        height = data["height"]
        weight = data["weight"]

        species_response = requests.get(data["species"]["url"])
        species_data = species_response.json()

        description = None
        for entry in species_data["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                break

        evolution_chain = []

        evolution_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_url)
        evolution_data = evolution_response.json()

        def extract_evolutions(chain):
            evolution_chain.append(chain["species"]["name"])

            if chain["evolves_to"]:
                for evo in chain["evolves_to"]:
                    extract_evolutions(evo)

        extract_evolutions(evolution_data["chain"])

        return {
            "name": data["name"],
            "types": types,
            "abilities": abilities,
            "stats": stats,
            "moves": moves,
            "height": height,
            "weight": weight,
            "description": description,
            "evolutions": evolution_chain
        }