from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI

from utils.db import db

def crear_app():
    app = Flask(__name__)

    app.secret_key = "secretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.items import items
    app.register_blueprint(items)

    return app

appcreada = crear_app()
