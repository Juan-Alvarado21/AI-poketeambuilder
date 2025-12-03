from flask import render_template, request, jsonify
from app.data_loader import load_pokemon_data
from app.services import get_all_pokemon, generate_recommendations

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/get_pokemon_list', methods=['GET'])
    def get_pokemon_list():
        try:
            load_pokemon_data()
            pokemon_list = get_all_pokemon()
            return jsonify({'pokemon': pokemon_list})
        except FileNotFoundError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Error al cargar Pokémon: {str(e)}'}), 500
    
    @app.route('/recommend', methods=['POST'])
    def recommend():
        try:
            load_pokemon_data()
            
            data = request.get_json()
            rival_names = data.get('rival_team', [])
            num_recommendations = int(data.get('num_recommendations', 5))
            team_size = int(data.get('team_size', 6))

            if not rival_names:
                return jsonify({'error': 'Debes seleccionar al menos un Pokémon rival'}), 400
            
            if len(rival_names) > 6:
                return jsonify({'error': 'No puedes seleccionar más de 6 Pokémon rivales'}), 400
            
            if team_size < 1:
                return jsonify({'error': 'El tamaño del equipo debe ser al menos 1'}), 400
            
            if team_size > 6:
                return jsonify({'error': 'El tamaño del equipo no puede ser mayor a 6'}), 400
            
            result = generate_recommendations(rival_names, num_recommendations, team_size)
            return jsonify(result)
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except FileNotFoundError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Error al procesar: {str(e)}'}), 500