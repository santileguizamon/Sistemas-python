from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
import random
import requests
from app.db.conexion import conectar
from config import HEADERS, JSONBIN_URL


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
    API_KEY = 'fb111263230578555f787dca0c591a8fe89e1aeb0665edde45daf8b3f29e8250'
    url = 'https://serpapi.com/search.json'

    departure_airports = ['PEK', 'LAX', 'JFK', 'ORD', 'SFO']
    arrival_airports = ['AUS', 'DFW', 'ATL', 'SEA', 'DEN']

    departure_id = random.choice(departure_airports)
    arrival_id = random.choice(arrival_airports)

    params = {
        'engine': 'google_flights',
        'departure_id': departure_id, 
        'arrival_id': arrival_id,    
        'outbound_date': '2024-10-29',
        'return_date': '2024-10-30',
        'currency': 'USD',
        'hl': 'en',
        'api_key': API_KEY
    }

    response = requests.get(url, params=params)

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
    API_KEY = 'fb111263230578555f787dca0c591a8fe89e1aeb0665edde45daf8b3f29e8250'
    url = "https://serpapi.com/search.json"

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
    
    if response.status_code != 200:
        return f"Error en la API: {response.status_code} - {response.text}"

    results = response.json()
    hotels = results.get('properties', [])

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
        "check_in_date": "2024-11-26",
        "check_out_date": "2024-11-30",
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


@busqueda_bp.route('/crear_vuelo', methods=['GET', 'POST'])
def crear_vuelo():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        fecha_ida = request.form['fecha_ida']
        fecha_vuelta = request.form['fecha_vuelta']
        horario_salida = request.form['horario_salida']
        horario_llegada = request.form['horario_llegada']
        pasajeros = request.form['pasajeros']

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO vuelos (origen, destino, fecha_ida, fecha_vuelta, horario_salida, horario_llegada, pasajeros)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (origen, destino, fecha_ida, fecha_vuelta, horario_salida, horario_llegada, pasajeros)
        )
        conexion.commit()
        conexion.close()

        flash('Vuelo creado con éxito')
        return redirect(url_for('busqueda.ver_vuelos'))

    return render_template('busqueda/crear_vuelo.html')

@busqueda_bp.route('/editar_vuelo/<int:id>', methods=['GET', 'POST'])
def editar_vuelo(id):
    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        fecha_ida = request.form['fecha_ida']
        fecha_vuelta = request.form['fecha_vuelta']
        horario_salida = request.form['horario_salida']
        horario_llegada = request.form['horario_llegada']
        pasajeros = request.form['pasajeros']

        cursor.execute("""
            UPDATE vuelos
            SET origen = ?, destino = ?, fecha_ida = ?, fecha_vuelta = ?, horario_salida = ?, horario_llegada = ?, pasajeros = ?
            WHERE id = ?""",
            (origen, destino, fecha_ida, fecha_vuelta, horario_salida, horario_llegada, pasajeros, id)
        )
        conexion.commit()
        conexion.close()

        flash('Vuelo actualizado con éxito')
        return redirect(url_for('busqueda.ver_vuelos'))
    else:
        cursor.execute("SELECT * FROM vuelos WHERE id = ?", (id,))
        vuelo = cursor.fetchone()
        conexion.close()

        return render_template('busqueda/editar_vuelo.html', vuelo=vuelo)

@busqueda_bp.route('/eliminar_vuelo/<int:id>', methods=['GET'])
def eliminar_vuelo(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM vuelos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

    flash('Vuelo eliminado con éxito')
    return redirect(url_for('busqueda.ver_vuelos'))

@busqueda_bp.route('/ver_vuelos')
@admin_required
def ver_vuelos():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Consulta para obtener todos los vuelos
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

    # Renderizar plantilla con los hoteles obtenidos
    return render_template('busqueda/ver_hoteles.html', hoteles=hoteles)