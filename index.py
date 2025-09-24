"""


from app import crear_app
from utils.db import db
import config
import os

app = crear_app()
db.init_app(app)
    
with app.app_context():
    db.create_all()
if __name__ == "__main__":


    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
        )


"""

import os
import logging

from flask import request

# Configurar logging para producción
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_application():
    #Factory function que funciona tanto en desarrollo como producción
    logger.info("🏭 Creando aplicación Flask...")
    
    # Importar factory function
    from app import crear_app
    app = crear_app()
    
    # Importar SQLAlchemy
    from utils.db import db
    
    # CRÍTICO: Inicializar SQLAlchemy dentro de application context
    logger.info("🔧 Inicializando SQLAlchemy...")
    db.init_app(app)
    
    # CRÍTICO: Crear tablas dentro de application context
    with app.app_context():
        logger.info("📋 Creando/verificando tablas...")
        try:
            db.create_all()
            logger.info("✅ Tablas creadas/verificadas exitosamente")
        except Exception as e:
            logger.error(f"❌ Error creando tablas: {e}")
            # No fallar aquí, dejar que la app trate de funcionar
    
    # IMPORTANTE: Registrar error handlers para debugging
    @app.errorhandler(500)
    def handle_500(e):
        logger.error(f"Error 500: {str(e)}")
        return "Error interno del servidor", 500
    
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.url}")
    
    logger.info("✅ Aplicación creada exitosamente")
    return app

def run_development():
    #Función para desarrollo local
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"🚀 Iniciando servidor de desarrollo en puerto {port}")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )

# CRÍTICO: Crear la aplicación a nivel de módulo
# Esto asegura que Gunicorn pueda acceder a 'app'
logger.info("🎬 Inicializando aplicación para Gunicorn...")
app = create_application()

# Solo para debugging - verificar que app está disponible
if app:
    logger.info(f"✅ App disponible: {app.name}")
else:
    logger.error("❌ App es None!")

if __name__ == "__main__":
    logger.info("🔧 Ejecutando en modo desarrollo...")
    run_development()
else:
    logger.info("🌐 Aplicación lista para Gunicorn")

    