import os
from flask import Flask
from app.data_loader import load_type_chart, preload_pokemon

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

def create_app():
    load_type_chart()
    preload_pokemon()
    return app
