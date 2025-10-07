
from flask import Blueprint, render_template
from models.items import Items

items = Blueprint("items", __name__)

@items.route('/')
def index():
    """
    Página principal - Formulario + Lista de productos
    """
    return render_template('index.html')

@items.route("/update/<id>")
def update_item(id):
    """
    Página con formulario para actualizar producto
    """
    return render_template('update.html', item_id=id)

@items.route("/about")
def about():
    """
    Página informativa
    """
    return render_template('about.html')
