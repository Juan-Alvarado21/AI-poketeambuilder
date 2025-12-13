import os
import pandas as pd
from app.utils import get_sprite_url

DATA_DIR = "data"
TYPE_CHART = {}
pokemon_data = None
POKEMON_LIST = []

def load_type_chart():
    global TYPE_CHART
    path = os.path.join(DATA_DIR, "type_chart.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("type_chart.csv no encontrado")
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower().str.strip()
    TYPE_CHART.clear()
    for _, row in df.iterrows():
        atk = row["attack_type"].lower()
        dfn = row["defense_type"].lower()
        mult = float(row["multiplier"])
        TYPE_CHART.setdefault(atk, {})[dfn] = mult

def preload_pokemon():
    global pokemon_data, POKEMON_LIST
    path = os.path.join(DATA_DIR, "poke.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("poke.csv no encontrado")
    pokemon_data = pd.read_csv(path)
    pokemon_data.columns = pokemon_data.columns.str.lower().str.strip()
    POKEMON_LIST.clear()
    for _, row in pokemon_data.iterrows():
        POKEMON_LIST.append({
            "nombre": row["nombre"],
            "tipo1": row["tipo1"],
            "tipo2": row["tipo2"] if pd.notna(row["tipo2"]) else "",
            "totalstats": int(row["totalstats"]),
            "sprite_url": get_sprite_url(row["nombre"]),
        })

try:
    load_type_chart()
    preload_pokemon()
    print(f"Datos cargados correctamente: {len(pokemon_data)} Pokémon")
except Exception as e:
    print(f"ERROR al cargar datos: {e}")
    raise