#from app import crear_app
#from utils.db import db
#import config
#import os

#app = crear_app()

#with app.app_context():
#    db.create_all()

#if __name__ == "__main__":
    
    
#    port = int(os.environ.get("PORT", 5000))
#    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
#    app.run(
#        host="0.0.0.0",
#        port=port,
#        debug=debug_mode
#        )


# main.py - Versión con debugging para encontrar el problema

import os
import sys
import traceback

# Agregar logging para debugging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("🚀 Iniciando aplicación...")
    logger.info(f"🐍 Python version: {sys.version}")
    logger.info(f"📂 Working directory: {os.getcwd()}")
    logger.info(f"📋 Files in directory: {os.listdir('.')}")
    
    # Intentar imports uno por uno para encontrar el problema
    logger.info("📦 Importando módulos...")
    
    try:
        from app import crear_app
        logger.info("✅ app importado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error importando app: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    try:
        from utils.db import db
        logger.info("✅ db importado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error importando db: {e}")
        traceback.print_exc()
        # No salir aquí, continuar sin db si es necesario
    
    try:
        import config
        logger.info("✅ config importado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error importando config: {e}")
        traceback.print_exc()
    
    # Verificar variables de entorno críticas
    logger.info("🔧 Verificando variables de entorno...")
    env_vars = ['Usuario_BD', 'Password_BD', 'Host_BD', 'Puerto_BD', 'Nombre_BD']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"✅ {var}: configurada")
        else:
            logger.warning(f"⚠️ {var}: NO configurada")
    


    
    logger.info("🎯 Configurando base de datos...")
    try:
        app = crear_app()
        logger.info("✅ DB inicializada")
        
        with app.app_context():
            db.create_all()
            logger.info("✅ Tablas creadas/verificadas")
    except Exception as e:
        logger.error(f"❌ Error con base de datos: {e}")
        traceback.print_exc()
        # Continuar sin DB para ver si es el problema

    # Verificar si app es válida
    if app:
        logger.info(f"✅ App object: {type(app)}")
        logger.info(f"✅ App name: {app.name}")
    else:
        logger.error("❌ App is None!")
        sys.exit(1)    
    logger.info("✅ Aplicación configurada exitosamente")
    
except Exception as e:
    logger.error(f"💥 Error fatal durante startup: {e}")
    traceback.print_exc()
    sys.exit(1)

def run_app():
    """Función para desarrollo"""
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"🚀 Iniciando servidor en puerto {port}, debug={debug_mode}")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )

if __name__ == "__main__":
    logger.info("🎬 Ejecutando en modo desarrollo...")
    run_app()
else:
    logger.info("🌐 Ejecutando en modo producción (Gunicorn)")
    logger.info("✅ App lista para Gunicorn")