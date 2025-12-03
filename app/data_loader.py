import pandas as pd
import os

TYPE_CHART = {}
pokemon_data = None

def load_type_chart():
    global TYPE_CHART
    file_path = os.path.join('data', 'type_chart.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Archivo {file_path} no encontrado en el directorio del servidor')
    
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.strip()
    
    TYPE_CHART = {}
    for _, row in df.iterrows():
        attack_type = row['attack_type'].lower().strip()
        defense_type = row['defense_type'].lower().strip()
        multiplier = float(row['multiplier'])
        
        if attack_type not in TYPE_CHART:
            TYPE_CHART[attack_type] = {}
        TYPE_CHART[attack_type][defense_type] = multiplier
    
    return TYPE_CHART

def load_pokemon_data():
    global pokemon_data
    
    if pokemon_data is None:
        file_path = os.path.join('data', 'poke.csv')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Archivo {file_path} no encontrado')
        
        pokemon_data = pd.read_csv(file_path)
        pokemon_data.columns = pokemon_data.columns.str.lower().str.strip()
    
    return pokemon_data

def get_type_chart():
    global TYPE_CHART
    return TYPE_CHART

def get_pokemon_data():
    global pokemon_data
    return pokemon_data