import pandas as pd
from app.data_loader import get_type_chart, get_pokemon_data
from app.utils import get_sprite_url

def calculate_effectiveness(attacker_types, defender_types):
    TYPE_CHART = get_type_chart()
    total = 1.0
    
    for atk_type in attacker_types:
        if atk_type and atk_type in TYPE_CHART:
            for def_type in defender_types:
                if def_type and TYPE_CHART[atk_type].get(def_type):
                    total *= TYPE_CHART[atk_type][def_type]
    
    return total

def get_pokemon_types(pokemon_name):
    pokemon_data = get_pokemon_data()
    pokemon = pokemon_data[pokemon_data['nombre'].str.lower() == pokemon_name.lower()]
    
    if pokemon.empty:
        return None
    
    types = [pokemon.iloc[0]['tipo1']]
    if pd.notna(pokemon.iloc[0]['tipo2']) and pokemon.iloc[0]['tipo2']:
        types.append(pokemon.iloc[0]['tipo2'])
    
    return types

def calculate_team_score(candidate_name, rival_team_types):
    pokemon_data = get_pokemon_data()
    candidate = pokemon_data[pokemon_data['nombre'] == candidate_name].iloc[0]
    
    candidate_types = [candidate['tipo1']]
    if pd.notna(candidate['tipo2']) and candidate['tipo2']:
        candidate_types.append(candidate['tipo2'])
    
    type_score = 0
    for rival_types in rival_team_types:
        eff = calculate_effectiveness(candidate_types, rival_types)
        if eff >= 2.0:
            type_score += 3
        elif eff > 1.0:
            type_score += 1.5
        elif eff == 0:
            type_score -= 1
    
    stats_score = candidate['totalstats'] / 100
    return (type_score * 0.6) + (stats_score * 0.4)

def generate_teams(all_scores, num_teams=5, team_size=6):
    teams = []
    
    for t in range(num_teams):
        team = []
        used_pokemon = set()
        used_type_combos = {}
        start_index = t * 2
        
        for i in range(start_index, len(all_scores)):
            if len(team) >= team_size:
                break
            
            pokemon = all_scores[i]
            type_combo = f"{pokemon['tipo1']}-{pokemon.get('tipo2', '')}"
            
            if pokemon['nombre'] not in used_pokemon:
                type_count = used_type_combos.get(type_combo, 0)
                max_same_type = 1 if len(team) < 3 else 2
                
                if type_count < max_same_type:
                    team.append(pokemon)
                    used_pokemon.add(pokemon['nombre'])
                    used_type_combos[type_combo] = type_count + 1
        
        if len(team) == team_size:
            teams.append(team)
        
        if len(teams) >= num_teams:
            break
    
    return teams

def get_all_pokemon():
    pokemon_data = get_pokemon_data()
    pokemon_list = []
    
    for _, row in pokemon_data.iterrows():
        tipo2 = row['tipo2'] if pd.notna(row['tipo2']) else ''
        pokemon_list.append({
            'nombre': row['nombre'],
            'tipo1': row['tipo1'],
            'tipo2': tipo2,
            'totalstats': int(row['totalstats']),
            'sprite_url': get_sprite_url(row['nombre'])
        })
    
    return pokemon_list

def generate_recommendations(rival_names, num_recommendations=5, team_size=6):
    pokemon_data = get_pokemon_data()
    
    # Obtener tipos del equipo rival
    rival_team_types = []
    rival_team_display = []
    
    for name in rival_names:
        types = get_pokemon_types(name)
        if types:
            rival_team_types.append(types)
            pokemon = pokemon_data[pokemon_data['nombre'].str.lower() == name.lower()].iloc[0]
            rival_team_display.append({
                'name': name,
                'types': types,
                'totalstats': int(pokemon['totalstats']),
                'sprite_url': get_sprite_url(name)
            })
        else:
            raise ValueError(f'Pokémon "{name}" no encontrado')

    strong_pokemon = pokemon_data[pokemon_data['totalstats'] >= 450].copy()
    
    scores = []
    for _, pokemon in strong_pokemon.iterrows():
        if pokemon['nombre'] not in rival_names:
            score = calculate_team_score(pokemon['nombre'], rival_team_types)
            scores.append({
                'nombre': pokemon['nombre'],
                'tipo1': pokemon['tipo1'],
                'tipo2': pokemon['tipo2'] if pd.notna(pokemon['tipo2']) else '',
                'totalstats': int(pokemon['totalstats']),
                'score': score,
                'sprite_url': get_sprite_url(pokemon['nombre'])
            })
    
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    
    teams = generate_teams(scores, num_recommendations, team_size)
    
    teams_response = []
    for team in teams:
        avg_stats = sum(p['totalstats'] for p in team) / len(team)
        avg_score = sum(p['score'] for p in team) / len(team)
        teams_response.append({
            'pokemon': team,
            'avg_stats': avg_stats,
            'avg_score': avg_score
        })
    
    return {
        'rival_team': rival_team_display,
        'teams': teams_response
    }