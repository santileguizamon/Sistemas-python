from flask import Blueprint, render_template,url_for,request,redirect

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')

@busqueda_bp.route('/index')
def  index():
    return render_template('busqueda/index.html')

@busqueda_bp.route('/indexHotel')
def   indexHotel():
    return render_template('busqueda/indexHotel.html')

@busqueda_bp.route('/buscadorVuelo')
def buscadorVuelo():
    vuelo_ida = {
        "origen": "España",
        "destino": "Francia",
        "fecha_salida": "2024-07-26",
        "hora_salida": "10:00 AM",
        "hora_llegada": "12:00 PM",
        "tipo_vuelo": "Directo"
    }
    vuelo_vuelta = {
        "origen": "Francia",
        "destino": "España",
        "fecha_salida": "2024-07-30",
        "hora_salida": "14:00 PM",
        "hora_llegada": "16:00 PM",
        "tipo_vuelo": "Con Escala"
    }
    return render_template('busqueda/buscadorVuelo.html', vuelo_ida=vuelo_ida, vuelo_vuelta=vuelo_vuelta)

@busqueda_bp.route('/buscadorHotel')
def buscadorHotel():
    return render_template('busqueda/busquedaHotel.html')