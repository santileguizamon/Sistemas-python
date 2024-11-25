from flask import Blueprint, render_template, request
from datetime import datetime
import sqlite3
import random
import requests
from app.db.conexion import conectar


from config import HEADERS, JSONBIN_URL

def conectar():
    return sqlite3.connect('agencia_viajes.db')

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')


@busqueda_bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('busqueda/index.html')


@busqueda_bp.route('/indexUsuarioAdministrador')
def  indexUsuarioAdministrador():
    return render_template('busqueda/indexUsuarioAdministrador.html')


@busqueda_bp.route('/indexHotel')
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
    return render_template('busqueda/busquedaHotel.html')
    

@busqueda_bp.route('/buscarVuelo')
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

    if response.status_code == 200:
        data = response.json()
        best_flights = data.get('best_flights', [])
        return render_template('busqueda/buscarVuelo.html', best_flights=best_flights, departure_id=departure_id, arrival_id=arrival_id)
    else:
        error_message = f'Error: {response.status_code} - {response.text}'
        return render_template('busqueda/buscarVuelo.html', error=error_message)


@busqueda_bp.route('/buscarHotel')
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
def ver_vuelos():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Consulta para obtener todos los vuelos
    cursor.execute('SELECT * FROM vuelos')
    vuelos = cursor.fetchall()
    
    conexion.close()
    
    return render_template('busqueda/ver_vuelos.html', vuelos=vuelos)

@busqueda_bp.route('/ver_hoteles', methods=['GET'])
def ver_hoteles():
    conexion = conectar()
    cursor = conexion.cursor()

    # Consulta para obtener todos los hoteles
    cursor.execute('SELECT nombre, descripcion, habitaciones FROM hoteles')
    hoteles = cursor.fetchall()

    conexion.close()

    # Renderizar plantilla con los hoteles obtenidos
    return render_template('busqueda/ver_hoteles.html', hoteles=hoteles)