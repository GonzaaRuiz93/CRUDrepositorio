from utils.db import db



class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column (db.String(50))
    stock = db.Column (db.Integer)
    precio = db.Column (db.Float)

    def __init__(self, nombre, stock, precio):
        self.nombre = nombre
        self.stock = stock
        self.precio = precio


