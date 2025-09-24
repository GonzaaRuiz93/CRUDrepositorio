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

def initialize_app():
    #Inicializar aplicación con orden correcto
    
    # OPCIÓN A: Si app.py tiene create_app (factory pattern)
    try:
        from app import crear_app
        print("🏭 Usando factory pattern...")
        app = crear_app()  # Llamar a la función
    except ImportError:
        # OPCIÓN B: Si app.py tiene instancia directa
        from app import app
        print("📱 Usando instancia directa...")
    
    # Verificar que app es una instancia de Flask
    from flask import Flask
    if not isinstance(app, Flask):
        raise TypeError(f"app debe ser una instancia de Flask, pero es: {type(app)}")
    
    # Inicializar SQLAlchemy
    print("🔧 Inicializando SQLAlchemy...")
    from utils.db import db
    db.init_app(app)
    
    # Crear tablas
    with app.app_context():
        print("📋 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas/verificadas")
    
    return app

def run_development():
    #Función para desarrollo
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    print(f"🚀 Iniciando servidor en puerto {port}, debug={debug_mode}")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )

# CRÍTICO: Inicializar antes de que Gunicorn intente usar la app
print("🎬 Inicializando aplicación...")
app = initialize_app()
print("✅ Aplicación inicializada correctamente")

if __name__ == "__main__":
    print("🚀 Ejecutando en modo desarrollo...")
    run_development()
else:
    print("🌐 App lista para Gunicorn en producción")

    