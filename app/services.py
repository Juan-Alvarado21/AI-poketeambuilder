from app.data_loader import TYPE_CHART, pokemon_data
import pandas as pd

def calculate_effectiveness(attacker_types, defender_types):
    total = 1.0
    for atk in attacker_types:
        if atk is None or (isinstance(atk, float) and pd.isna(atk)):
            continue
        atk = atk.lower()
        for dfn in defender_types:
            if dfn is None or (isinstance(dfn, float) and pd.isna(dfn)):
                continue
            dfn = dfn.lower()
            total *= TYPE_CHART.get(atk, {}).get(dfn, 1)
    return total

def get_pokemon_types(name):
    p = pokemon_data[
        pokemon_data["nombre"].str.lower() == name.lower()
    ]
    if p.empty:
        return None
    row = p.iloc[0]
    
    if pd.notna(row["tipo2"]):
        return [row["tipo1"], row["tipo2"]]
    return [row["tipo1"]]

def calculate_team_score(candidate_name, rival_team_types):
    p = pokemon_data[
        pokemon_data["nombre"].str.lower() == candidate_name.lower()
    ].iloc[0]
    
    types = [p["tipo1"]]
    if pd.notna(p["tipo2"]):
        types.append(p["tipo2"])
    
    type_score = 0
    for rival_types in rival_team_types:
        eff = calculate_effectiveness(types, rival_types)
        if eff >= 2:
            type_score += 3
        elif eff > 1:
            type_score += 1.5
        elif eff == 0:
            type_score -= 1
    
    stats_score = p["totalstats"] / 100
    return type_score * 0.6 + stats_score * 0.4

def generate_teams(scores, num_teams, team_size):
    teams = []
    for t in range(num_teams):
        team = []
        used = set()
        start = t * 2
        for i in range(start, len(scores)):
            if len(team) >= team_size:
                break
            p = scores[i]
            if p["nombre"] not in used:
                team.append(p)
                used.add(p["nombre"])
        if len(team) == team_size:
            teams.append(team)
    return teams