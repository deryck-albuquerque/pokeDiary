import pokepy

class Pokemon:

    @staticmethod
    def get_pokemon_type(name: str) -> str:
        client = pokepy.V2Client()
        pokemon_type = client.get_type("pikachu")

        return pokemon_type