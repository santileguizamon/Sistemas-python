from flask import Blueprint, render_template, request
from datetime import datetime
import sqlite3
import random
import requests
from app.db.conexion import conectar


from config import HEADERS, JSONBIN_URL
from decorador.decorators import admin_required

def conectar():
    return sqlite3.connect('agencia_viajes.db')

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')


@busqueda_bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('busqueda/index.html')


@busqueda_bp.route('/indexUsuarioAdministrador')
@admin_required
def  indexUsuarioAdministrador():
    return render_template('busqueda/indexUsuarioAdministrador.html')


@busqueda_bp.route('/indexHotel',methods=['GET', 'POST'])
def   indexHotel():
    return render_template('busqueda/indexHotel.html')


@busqueda_bp.route('/buscadorVuelo', methods=['GET', 'POST'])
def buscadorVuelo():
    origen = request.form.get('origen', '').strip()
    destino = request.form.get('destino', '').strip()
    fecha_ida = request.form.get('fecha-ida', '')
    fecha_vuelta = request.form.get('fecha-vuelta', '')

    conexion = conectar()
    cursor = conexion.cursor()

    query = '''
    SELECT nombre_avion, horario_salida, horario_llegada, precio
    FROM vuelos
    WHERE 1=1
    '''
    params = []

    if origen:
        query += " AND origen_id = (SELECT id FROM lugares WHERE nombre = ?)"
        params.append(origen)

    if destino:
        query += " AND destino_id = (SELECT id FROM lugares WHERE nombre = ?)"
        params.append(destino)

    if fecha_ida:
        query += " AND DATE(horario_salida) = ?"
        params.append(fecha_ida)

    if fecha_vuelta:
        query += " AND DATE(horario_llegada) = ?"
        params.append(fecha_vuelta)

    cursor.execute(query, params)
    vuelos = cursor.fetchall()

    conexion.close()

    return render_template('busqueda/buscadorVuelo.html', vuelos=vuelos)


@busqueda_bp.route('/buscadorHotel', methods=['GET','POST'])
def buscadorHotel():
    destino = request.form.get('destino', '').strip()
    fecha_ida = request.form.get('fecha-ida', '')
    fecha_vuelta = request.form.get('fecha-vuelta', '')
    personas = request.form.get('habitaciones', '').strip()

    conexion = conectar()
    cursor = conexion.cursor()

    query = '''
    SELECT destino, fecha_ida, fecha_vuelta, habitaciones
    FROM vuelos
    WHERE 1=1
    '''
    params = []


    if destino:
        query += " AND lugar_id = (SELECT id FROM lugares WHERE nombre = ?)"
        params.append(destino)

    if fecha_ida:
        query += " AND DATE(horario_salida) = ?"
        params.append(fecha_ida)

    if fecha_vuelta:
        query += " AND DATE(horario_llegada) = ?"
        params.append(fecha_vuelta)

    cursor.execute(query, params)
    hoteles = cursor.fetchall()

    conexion.close()


    return render_template('busqueda/busquedaHotel.html', hoteles=hoteles)
    

@busqueda_bp.route('/buscarVuelo', methods=['GET','POST'])
def buscarVuelo():
    origen = request.form.get('origen', '').strip()
    destino = request.form.get('destino', '').strip()
    fecha_ida = request.form.get('fecha-ida', '')
    fecha_vuelta = request.form.get('fecha-vuelta', '')
    pasajeros = request.form.get('pasajeros', '').strip()

    conexion = conectar()
    cursor = conexion.cursor()

    query = '''
    SELECT origen, destino, fecha_ida, fecha_vuelta, horario_salida, horario_llegada, pasajeros
    FROM vuelos
    WHERE 1=1
    '''
    params = []

    if origen:
        query += " AND origen = ?"
        params.append(origen)

    if destino:
        query += " AND destino = ?"
        params.append(destino)

    if fecha_ida:
        query += " AND DATE(fecha_ida) = ?"
        params.append(fecha_ida)

    if fecha_vuelta:
        query += " AND DATE(fecha_vuelta) = ?"
        params.append(fecha_vuelta)

    if pasajeros:
        query += " AND pasajeros >= ?"
        params.append(pasajeros)

    try:
        cursor.execute(query, params)
        vuelos = cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar vuelos: {e}")
        vuelos = []

    conexion.close()

    return render_template('busqueda/busquedaVuelos.html', vuelos=vuelos)


@busqueda_bp.route('/buscarHotel', methods=['GET','POST'])
def buscarHotel():
      if request.method == 'POST':

        destino = request.form.get('destino', '').strip()
        fecha_entrada = request.form.get('fecha-entrada', '').strip()
        fecha_salida = request.form.get('fecha-salida', '').strip()
        habitaciones = request.form.get('habitaciones', '').strip()

        conexion = conectar()
        cursor = conexion.cursor()

        query = '''
        SELECT h.nombre, h.lugar, h.descripcion, h.imagen, h.habitaciones_disponibles
        FROM hoteles h
        WHERE 1=1
        '''
        params = []

        if destino:
            query += " AND h.lugar = ?"
            params.append(destino)
        
        if fecha_entrada and fecha_salida:
            query += '''
            AND NOT EXISTS (
                SELECT 1
                FROM reservas r
                WHERE r.hotel_id = h.id
                AND (
                    (r.fecha_entrada <= ? AND r.fecha_salida >= ?)
                    OR (r.fecha_entrada <= ? AND r.fecha_salida >= ?)
                )
            )
            '''
            params.extend([fecha_salida, fecha_entrada, fecha_salida, fecha_entrada])

        if habitaciones:
            query += " AND h.habitaciones_disponibles >= ?"
            params.append(habitaciones)

        cursor.execute(query, params)
        hotels = cursor.fetchall()


        conexion.close()


        return render_template('busqueda/buscarHotel.html', hotels=hotels)

   
 



@busqueda_bp.route('/buscar_Precios_de_Vuelos')
@admin_required
def buscar_Precios_de_Vuelos():

    price_insights = {
        "lowest_price": 1339,
        "price_level": "high",
        "typical_price_range": [570, 1050],
        "price_history": [
            [1691013600, 575],
            [1691100000, 575],
            [1696111200, 1199],
            [1696197600, 1339]
        ]
    }

    if not price_insights:

        return render_template('busqueda/buscar_Precios_de_Vuelos.html', price_insights={})

    return render_template('busqueda/buscar_Precios_de_Vuelos.html', price_insights=price_insights)


@busqueda_bp.route('/buscar_Precios_de_Hoteles')
@admin_required
def buscar_Precios_de_Hoteles():
    API_KEY = 'fb111263230578555f787dca0c591a8fe89e1aeb0665edde45daf8b3f29e8250'
    url = 'https://serpapi.com/search.json'

    params = {
        "engine": "google_hotels",
        "q": "Bali Resorts",
        "check_in_date": "2024-10-29",
        "check_out_date": "2024-10-30",
        "adults": 2,
        "currency": "USD",
        "gl": "us",
        "hl": "en",
        'api_key': API_KEY
    }

    response = requests.get(url, params=params)
    results = response.json()

    hotels = results.get('properties', [])
    
    return render_template('busqueda/buscar_Precios_de_Hoteles.html', hotels=hotels)

@busqueda_bp.route('/ver_vuelos')
@admin_required
def ver_vuelos():
    conexion = conectar()
    cursor = conexion.cursor()
    
 
    cursor.execute('SELECT * FROM vuelos')
    vuelos = cursor.fetchall()
    
    conexion.close()
    

    return render_template('busqueda/ver_vuelos.html', vuelos=vuelos)

@busqueda_bp.route('/ver_hoteles', methods=['GET'])
@admin_required
def ver_hoteles():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('SELECT nombre, descripcion, habitaciones FROM hoteles')
    hoteles = cursor.fetchall()

    conexion.close()

 
    return render_template('busqueda/ver_hoteles.html', hoteles=hoteles)