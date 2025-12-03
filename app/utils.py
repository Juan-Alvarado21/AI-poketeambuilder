import requests

def normalize_pokemon_name(name):
    return name.lower().replace(' ', '-').replace('.', '-')

def get_sprite_url(pokemon_name):
    """Obtiene la URL del sprite de un Pokémon"""
    normalized = normalize_pokemon_name(pokemon_name)
    primary = f"https://img.pokemondb.net/sprites/scarlet-violet/normal/{normalized}.png"
    fallback = f"https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{normalized}.png"
    
    try:
        r = requests.head(primary)
        if r.status_code == 200:
            return primary
    except:
        pass
    
    return fallback