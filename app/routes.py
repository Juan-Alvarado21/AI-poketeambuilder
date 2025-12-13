from flask import render_template, request, jsonify
from app import app
from app.data_loader import POKEMON_LIST, pokemon_data
from app.services import (
    get_pokemon_types,
    calculate_team_score,
    generate_teams,
)
from app.utils import get_sprite_url
import pandas as pd
import math
import json


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_pokemon_list")
def get_pokemon_list():
    return jsonify({"pokemon": POKEMON_LIST})


def sanitize_value(val):
    """Convierte NaN, Infinity y otros valores problemáticos a valores válidos"""
    if val is None:
        return 0
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return 0
    return val


def sanitize_sprite_url(sprite_url):
    """Asegura que sprite_url sea un formato JSON válido"""
    if sprite_url is None:
        return ""
    if isinstance(sprite_url, dict):
        return sprite_url
    if isinstance(sprite_url, str):
        return sprite_url
    return ""


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    rival_names = data.get("rival_team", [])
    num_rec = int(data.get("num_recommendations", 5))
    team_size = int(data.get("team_size", 6))
    
    if not rival_names:
        return jsonify({"error": "Debes seleccionar al menos un Pokémon"}), 400
    
    rival_team_types = []
    display_rival = []
    
    for name in rival_names:
        types = get_pokemon_types(name)
        if not types:
            return jsonify({"error": f'Pokémon "{name}" no encontrado'}), 400
        
        p = pokemon_data[
            pokemon_data["nombre"].str.lower() == name.lower()
        ].iloc[0]
        
        rival_team_types.append(types)
        
        clean_types = [str(t) for t in types if pd.notna(t)]
        
        display_rival.append({
            "name": str(name),
            "types": clean_types,
            "totalstats": int(p["totalstats"]),
            "sprite_url": sanitize_sprite_url(get_sprite_url(name)),
        })
    
    strong = pokemon_data[pokemon_data["totalstats"] >= 450]
    scores = []
    
    for _, p in strong.iterrows():
        if p["nombre"] not in rival_names:
            score = calculate_team_score(p["nombre"], rival_team_types)
            score = sanitize_value(score)
            
            tipo2_value = ""
            if pd.notna(p["tipo2"]) and p["tipo2"]:
                tipo2_value = str(p["tipo2"])
            
            scores.append({
                "nombre": str(p["nombre"]),
                "tipo1": str(p["tipo1"]),
                "tipo2": tipo2_value,
                "totalstats": int(p["totalstats"]),
                "score": float(score),
                "sprite_url": sanitize_sprite_url(get_sprite_url(p["nombre"])),
            })
    
    scores.sort(key=lambda x: x["score"], reverse=True)
    teams_raw = generate_teams(scores, num_rec, team_size)
    
    teams = []
    for team in teams_raw:
        if team:
            avg_stats = sum(p["totalstats"] for p in team) / len(team)
            avg_score = sum(sanitize_value(p["score"]) for p in team) / len(team)
            
            teams.append({
                "pokemon": team,
                "avg_stats": float(sanitize_value(avg_stats)),
                "avg_score": float(sanitize_value(avg_score)),
            })
    
    response = {
        "rival_team": display_rival,
        "teams": teams,
    }
    
    return jsonify(response)