
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


app = iniciar_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )

   