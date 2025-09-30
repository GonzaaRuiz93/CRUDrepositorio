"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.items import Items
from utils.db import db


items = Blueprint("items", __name__)


@items.route('/')
def index():
"""
"""
    Obtener lista de productos
    ---
    tags:
      - Items
    responses:
      200:
        description: Lista de productos ordenados por ID descendente
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
                example: "Laptop"
              stock:
                type: integer
                example: 10
              precio:
                type: number
                format: float
                example: 599.99
    """
"""
    items = Items.query.order_by(Items.id.desc()).all()
    return render_template('index.html', items=items)

@items.route("/new", methods=['POST'])
def add_item():
"""
"""
    Crear un nuevo producto
    ---
    tags:
      - Items
    parameters:
      - name: nombre
        in: formData
        type: string
        required: true
        description: Nombre del producto
        example: "Mouse Gamer"
      - name: stock
        in: formData
        type: integer
        required: true
        description: Cantidad en stock
        example: 25
      - name: precio
        in: formData
        type: string
        required: true
        description: Precio del producto (acepta coma o punto)
        example: "49,99"
    responses:
      302:
        description: Producto creado exitosamente, redirige a index
      400:
        description: Datos inválidos
    """
"""
    nombre=request.form['nombre']
    stock=int(request.form['stock'])
    reemplazar = request.form['precio']
    precio = float(reemplazar.replace(",", "."))  # Permite que el precio acepte coma o punto

    #guardar en base de datos
    ItemNuevo=Items(nombre, stock, precio)
    db.session.add(ItemNuevo)
    db.session.commit() 

    flash("Producto añadido satisfactoriamente")

    #redirecciona a la pagina inicial
    return redirect(url_for('items.index'))

@items.route("/update/<id>", methods=['POST', 'GET'])
def update_item(id):
"""
"""
    Actualizar un producto existente
    ---
    tags:
      - Items
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a actualizar
        example: 5
      - name: nombre
        in: formData
        type: string
        required: false
        description: Nuevo nombre del producto
      - name: stock
        in: formData
        type: integer
        required: false
        description: Nueva cantidad en stock
      - name: precio
        in: formData
        type: string
        required: false
        description: Nuevo precio
    responses:
      200:
        description: Formulario de actualización (GET)
      302:
        description: Producto actualizado exitosamente (POST)
      404:
        description: Producto no encontrado
    """
"""    
    item=Items.query.get(id) #obteniendo ID

    if request.method == 'POST':
        
        item.nombre = request.form["nombre"]
        item.stock = request.form["stock"]
        item.precio = request.form["precio"]

        db.session.commit()

        flash("Producto actualizado satisfactoriamente")

        return redirect(url_for('items.index'))
    
    return render_template('update.html', item=item)

@items.route("/delete/<id>")
def delete_item(id):
"""
"""
    Eliminar un producto
    ---
    tags:
      - Items
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
        example: 3
    responses:
      302:
        description: Producto eliminado exitosamente, redirige a index
      404:
        description: Producto no encontrado
    """
"""
    item=Items.query.get(id) #obteniendo ID
    db.session.delete(item) #borrando producto
    db.session.commit()

    flash("Producto eliminado satisfactoriamente")

    #redirecciona a la pagina inicial
    return redirect(url_for('items.index'))

@items.route("/about")
def about():
"""
"""
    Página de información
    ---
    tags:
      - General
    responses:
      200:
        description: Página sobre el proyecto
    """
"""
    return render_template('about.html')

"""

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
