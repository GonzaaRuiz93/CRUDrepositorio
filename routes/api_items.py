

from flask import Blueprint, jsonify, request
from models.items import Items
from utils.db import db

api_items = Blueprint("api_items", __name__, url_prefix="/api")

# GET /api/items - Listar todos los productos
@api_items.route('/items', methods=['GET'])
def get_items():
    """
    Obtener lista de productos (JSON)
    ---
    tags:
      - API Items
    responses:
      200:
        description: Lista de productos en formato JSON
    """
    try:
        items = Items.query.order_by(Items.id.desc()).all()
        return jsonify({
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "stock": item.stock,
                    "precio": float(item.precio)
                } for item in items
            ],
            "count": len(items)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

"""
# GET /api/items/<id> - Obtener un producto específico
@api_items.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    
    Obtener un producto específico (JSON)
    ---
    tags:
      - API Items
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Producto encontrado
      404:
        description: Producto no encontrado
    
    try:
        item = Items.query.get(id)
        if not item:
            return jsonify({"success": False, "error": "Producto no encontrado"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": item.id,
                "nombre": item.nombre,
                "stock": item.stock,
                "precio": float(item.precio)
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
"""

# POST /api/items - Crear nuevo producto
@api_items.route('/items', methods=['POST'])
def create_item():
    """
    Crear un nuevo producto (JSON)
    ---
    tags:
      - API Items
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - stock
            - precio
          properties:
            nombre:
              type: string
            stock:
              type: integer
            precio:
              type: number
    responses:
      201:
        description: Producto creado exitosamente
      400:
        description: Datos inválidos
    """
    try:
        data = request.get_json()
        
        # Validaciones
        if not data or not all(k in data for k in ("nombre", "stock", "precio")):
            return jsonify({"success": False, "error": "Faltan campos requeridos: nombre, stock, precio"}), 400
        
        # Crear producto
        nuevo_item = Items(
            nombre=data['nombre'],
            stock=int(data['stock']),
            precio=float(str(data['precio']).replace(",", "."))  # Acepta coma o punto
        )
        
        db.session.add(nuevo_item)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Producto añadido satisfactoriamente",
            "data": {
                "id": nuevo_item.id,
                "nombre": nuevo_item.nombre,
                "stock": nuevo_item.stock,
                "precio": float(nuevo_item.precio)
            }
        }), 201
        
    except ValueError as e:
        return jsonify({"success": False, "error": f"Formato de datos inválido: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


# PUT /api/items/<id> - Actualizar producto
@api_items.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    """
    Actualizar un producto existente (JSON)
    ---
    tags:
      - API Items
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            stock:
              type: integer
            precio:
              type: number
    responses:
      200:
        description: Producto actualizado exitosamente
      404:
        description: Producto no encontrado
    """
    try:
        item = Items.query.get(id)
        if not item:
            return jsonify({"success": False, "error": "Producto no encontrado"}), 404
        
        data = request.get_json()
        
        # Actualizar campos enviados
        if 'nombre' in data:
            item.nombre = data['nombre']
        if 'stock' in data:
            item.stock = int(data['stock'])
        if 'precio' in data:
            item.precio = float(str(data['precio']).replace(",", "."))
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Producto actualizado satisfactoriamente",
            "data": {
                "id": item.id,
                "nombre": item.nombre,
                "stock": item.stock,
                "precio": float(item.precio)
            }
        }), 200
        
    except ValueError as e:
        return jsonify({"success": False, "error": f"Formato de datos inválido: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


# DELETE /api/items/<id> - Eliminar producto
@api_items.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    """
    Eliminar un producto (JSON)
    ---
    tags:
      - API Items
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Producto eliminado exitosamente
      404:
        description: Producto no encontrado
    """
    try:
        item = Items.query.get(id)
        if not item:
            return jsonify({"success": False, "error": "Producto no encontrado"}), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Producto eliminado satisfactoriamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    

    