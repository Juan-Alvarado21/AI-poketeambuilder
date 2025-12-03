from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Registrar rutas
    from app.routes import register_routes
    register_routes(app)
    
    return app