""" 


from app import crear_app
from utils.db import db
import config
import os

import logging
logger = logging.getLogger(__name__)

logger.info("🏭 Creando aplicación Flask...")
app = crear_app()
logger.info("🔧 Inicializando SQLAlchemy...")
db.init_app(app)

logger.info("📋 Creando/verificando tablas...")
with app.app_context():
    db.create_all()
    logger.info("✅ Tablas creadas/verificadas exitosamente")


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"🚀 Iniciando servidor de desarrollo en puerto {port}")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
        )


"""

import os
from flask import request


def iniciar_app():
    from app import crear_app
    app = crear_app()
    
    from utils.db import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app


#def run_development():
#    port = int(os.environ.get("PORT", 5000))
#    debug_mode = os.environ.get("FLASK_ENV") == "development"

#    app.run(
#        host="0.0.0.0",
#        port=port,
#        debug=debug_mode
#    )


app = iniciar_app()

if __name__ == "__main__":
    #run_development()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )

   