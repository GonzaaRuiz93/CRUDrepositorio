from app import app
from utils.db import db
import config
import os


if __name__ == "__main__":
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
        )
    