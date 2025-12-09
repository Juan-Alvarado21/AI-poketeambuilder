SPRITE_CACHE = {}

def normalize_pokemon_name(name):
    return name.lower().replace(" ", "-").replace(".", "-")

def get_sprite_url(pokemon_name):
    normalized = normalize_pokemon_name(pokemon_name)
    if normalized in SPRITE_CACHE:
        return SPRITE_CACHE[normalized]
    primary = f"https://img.pokemondb.net/sprites/scarlet-violet/normal/{normalized}.png"
    fallback = f"https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{normalized}.png"
    SPRITE_CACHE[normalized] = {"primary": primary, "fallback": fallback}
    return SPRITE_CACHE[normalized]
