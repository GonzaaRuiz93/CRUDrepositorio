"""
from flask import Flask
from config import DATABASE_URI

from utils.db import db

def crear_app():
    app = Flask(__name__)

    app.secret_key = "secretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#    db.init_app(app)

    from routes.items import items
    app.register_blueprint(items)

    return app

app = crear_app


"""


from flask import Flask
import os
import logging
from config import DATABASE_URI

logger = logging.getLogger(__name__)

def crear_app():
    #Factory function para crear la aplicación Flask
    logger.info("🏭 Creando instancia de Flask...")
    
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # CRÍTICO: Configurar base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verificar conexiones antes de usar
        'pool_recycle': 300,    # Reciclar conexiones cada 5 minutos
    }
    
    logger.info(f"📊 Database URL configurada: {app.config['SQLALCHEMY_DATABASE_URI'][:20]}...")
    
   
    # Registrar rutas DESPUÉS de crear la app pero ANTES de inicializar DB
    register_blueprints(app)
    
    logger.info("✅ Aplicación Flask creada")
    return app

def register_blueprints(app):
    #Registrar todos los blueprints/rutas
    try:
        # IMPORTANTE: Importar DENTRO de la función para evitar circular imports
        from routes.items import items
        app.register_blueprint(items)
        logger.info("✅ Blueprint items registrado")
        
        # Si tienes más rutas:
        # from routes.users import users_bp
        # app.register_blueprint(users_bp)
        
    except ImportError as e:
        logger.error(f"❌ Error importando blueprints: {e}")
        raise

