

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


# GET /api/items/<id> - Obtener un producto específico
@api_items.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    """
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
    """
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
              description: Nombre del producto
              example: "Placa Madre ASUS"
            stock:
              type: integer
              description: Cantidad en inventario
              example: 15
              minimum: 0
            precio:
              type: number
              format: float
              description: Precio del producto (acepta coma o punto, sin símbolos monetarios)
              example: 5555.50
    responses:
      201:
        description: Producto creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Producto añadido satisfactoriamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: "Placa Madre ASUS"
                stock:
                  type: integer
                  example: 15
                precio:
                  type: number
                  example: 5555.50
      400:
        description: Datos inválidos o faltantes
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Faltan campos obligatorios: nombre, stock y precio son requeridos."
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Error inesperado en el servidor"
        """

    try:
        data = request.get_json()

        # Validaciones
        if not data:
            return jsonify({
                "success": False, 
                "error": "No se recibieron datos. Por favor completa el formulario."
            }), 400

        # Validar campos requeridos
        if not all(k in data for k in ("nombre", "stock", "precio")):
            return jsonify({
                "success": False, 
                "error": "Faltan campos obligatorios: nombre, stock y precio son requeridos."
            }), 400

        # Validar nombre no vacío
        if not data['nombre'] or data['nombre'].strip() == '':
            return jsonify({
                "success": False,
                "error": "El nombre del producto no puede estar vacío."
            }), 400

        # Validar y convertir stock
        try:
            stock = int(data['stock'])
            if stock < 0:
                return jsonify({
                    "success": False,
                    "error": "El stock debe ser un número entero positivo (Ej: 10, 20, 50)."
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "El stock debe ser un número entero. Ingresaste: " + str(data.get('stock'))
            }), 400

        # Validar y convertir precio
        try:
            precio_str = str(data['precio']).replace(",", ".").replace("$", "").replace("€", "").strip()
            precio = float(precio_str)
            if precio <= 0:
                return jsonify({
                    "success": False,
                    "error": "El precio debe ser mayor a cero."
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "El precio debe ser un número y no incluir ninguna letra u otro tipo de signo (Ej: 200.00). Ingresaste: " + str(data.get('precio'))
            }), 400

        # Crear producto
        nuevo_item = Items(
            nombre=data['nombre'].strip(),
            stock=stock,
            precio=precio
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

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False, 
            "error": f"Error inesperado en el servidor: {str(e)}"
        }), 500

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
        description: ID del producto a actualizar
        example: 5
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nuevo nombre del producto (opcional)
              example: "Placa Madre ASUS ROG"
            stock:
              type: integer
              description: Nueva cantidad en inventario (opcional)
              example: 20
              minimum: 0
            precio:
              type: number
              format: float
              description: Nuevo precio del producto (opcional, acepta coma o punto)
              example: 6500.75
    responses:
      200:
        description: Producto actualizado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Producto actualizado satisfactoriamente"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 5
                nombre:
                  type: string
                  example: "Placa Madre ASUS ROG"
                stock:
                  type: integer
                  example: 20
                precio:
                  type: number
                  example: 6500.75
      400:
        description: Datos inválidos
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "El precio debe ser mayor a cero."
      404:
        description: Producto no encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Producto no encontrado. ID: 5"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Error inesperado"
    """
    try:
        item = Items.query.get(id)
        if not item:
            return jsonify({
                "success": False, 
                "error": "Producto no encontrado. ID: " + str(id)
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No se recibieron datos para actualizar."
            }), 400

        # Actualizar nombre si viene
        if 'nombre' in data:
            if not data['nombre'] or data['nombre'].strip() == '':
                return jsonify({
                    "success": False,
                    "error": "El nombre del producto no puede estar vacío."
                }), 400
            item.nombre = data['nombre'].strip()

        # Actualizar stock si viene
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    return jsonify({
                        "success": False,
                        "error": "El stock debe ser un número entero positivo."
                    }), 400
                item.stock = stock
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": "El stock debe ser un número entero válido. Ingresaste: " + str(data.get('stock'))
                }), 400

        # Actualizar precio si viene
        if 'precio' in data:
            try:
                precio_str = str(data['precio']).replace(",", ".").replace("$", "").replace("€", "").strip()
                precio = float(precio_str)
                if precio <= 0:
                    return jsonify({
                        "success": False,
                        "error": "El precio debe ser mayor a cero."
                    }), 400
                item.precio = precio
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": "El precio debe ser un número y no incluir ninguna letra u otro tipo de signo (Ej: 200.00). Ingresaste: " + str(data.get('precio'))
                }), 400

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

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": f"Error inesperado: {str(e)}"
        }), 500

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
    
