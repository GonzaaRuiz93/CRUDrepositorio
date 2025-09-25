"""
from flask import Flask
from config import DATABASE_URI

from utils.db import db

import logging
logger = logging.getLogger(__name__)

def crear_app():
    logger.info("🏭 Creando instancia de Flask...")
    app = Flask(__name__)

    logger.info(f"📊 Configurando URL de base de datos")
    app.secret_key = "secretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    logger.info(f"📊 Database URL configurada: {app.config['SQLALCHEMY_DATABASE_URI'][:20]}...")
#    db.init_app(app)


    logger.info("Registrando Blueprint items...")
    from routes.items import items
    app.register_blueprint(items)
    logger.info("✅ Blueprint items registrado")

    logger.info("✅ Aplicación Flask creada, retornando...")
    return app

app = crear_app


"""


from flask import Flask
import os
from config import DATABASE_URI

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

    #register_blueprints(app)

    #Registrar Blueprint
    from routes.items import items
    app.register_blueprint(items)

    #BORRAR SI NO FUNCIONA
    from utils.db import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app

#def register_blueprints(app):
    #from routes.items import items
    #app.register_blueprint(items)


