"""from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.items import Items
from utils.db import db


items = Blueprint("items", __name__)


@items.route("/")
def index():
    items = Items.query.order_by(Items.id.desc()).all()

    return render_template('index.html', items=items)


@items.route('/')
def index():
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("🔍 Ejecutando consulta Items...")
    try:
        logger.info("📋 Intentando consulta a base de datos...")
        items = Items.query.order_by(Items.id.desc()).all()
        logger.info(f"✅ Consulta exitosa: {len(items)} items encontrados")
        return render_template('index.html', items=items)
    except Exception as e:
        logger.error(f"❌ Error en consulta: {e}")
        raise

@items.route("/new", methods=['POST'])
def add_item():
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
    item=Items.query.get(id) #obteniendo ID
    db.session.delete(item) #borrando producto
    db.session.commit()

    flash("Producto eliminado satisfactoriamente")

    #redirecciona a la pagina inicial
    return redirect(url_for('items.index'))

@items.route("/about")
def about():
    return render_template('about.html')


"""



# routes/items.py - Versión de debugging para verificar código actual

from flask import Blueprint, render_template, current_app
from models.items import Items
import logging
import datetime

logger = logging.getLogger(__name__)

items = Blueprint('items', __name__)

@items.route('/')
def index():
    # LÍNEA 10: Mensaje de debugging para confirmar versión
    logger.info("🚨 DEBUGGING: Esta es la NUEVA versión del código - " + str(datetime.datetime.now()))
    
    # Líneas 11-15: Más debugging
    logger.info("🔍 Iniciando función index()...")
    logger.info("📁 Archivo actual: routes/items.py")
    logger.info("🕐 Timestamp: " + str(datetime.datetime.now()))
    
    try:
        # Línea 16: Intentar la consulta
        logger.info("📊 Intentando consulta Items.query...")
        items = Items.query.order_by(Items.id.desc()).all()
        
        logger.info(f"✅ Consulta exitosa: {len(items)} items encontrados")
        return render_template('index.html', items=items)
        
    except Exception as e:
        logger.error(f"❌ Error en consulta: {str(e)}")
        logger.error(f"💥 Tipo de error: {type(e).__name__}")
        
        # Mostrar página de error simple en lugar de crash
        return f"<h1>Error de base de datos</h1><p>{str(e)}</p>", 500

# Ruta adicional para verificar que el código se actualizó
@items.route('/debug')
def debug_version():
    return f"""
    <h1>Debug Info</h1>
    <p><strong>Timestamp:</strong> {datetime.datetime.now()}</p>
    <p><strong>Archivo:</strong> routes/items.py</p>
    <p><strong>Línea 10:</strong> logger.info("🚨 DEBUGGING: Esta es la NUEVA versión...")</p>
    <p><strong>Status:</strong> Código actualizado correctamente</p>
    """