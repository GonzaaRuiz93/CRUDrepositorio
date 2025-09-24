from flask import Flask
from routes.items import items
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI

app = Flask(__name__)

app.secret_key = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(items)
