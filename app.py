
from flask import Flask
import os
from config import DATABASE_URI
from flasgger import Swagger

def crear_app():
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    #Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verificar conexiones antes de usar
        'pool_recycle': 300,    # Reciclar conexiones cada 5 minutos
    }

    # Configuración de Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "info": {
            "title": "CRUD de Items y API",
            "description": "API para gestión de inventario de productos de una tienda de electronicos. Incluye operaciones CRUD completas.",
            "version": "1.0.0",
            "contact": {
                "name": "Ve el codigo de mi CRUD en GitHub",
                "url": "https://github.com/GonzaaRuiz93/CRUDrepositorio"
            }
        },
        "schemes": [
            "https",
            "http"
        ]
    }
    
    # Inicializar Swagger
    Swagger(app, config=swagger_config, template=swagger_template)

    #Registrar Blueprint
    #from routes.items import items
    #app.register_blueprint(items)



    # Registrar Blueprints
    from routes.items import items
    from routes.api_items import api_items  # ← NUEVO
    
    app.register_blueprint(items)
    app.register_blueprint(api_items)  # ← NUEVO


    return app

