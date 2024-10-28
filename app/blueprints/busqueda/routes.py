from flask import Blueprint, render_template
from datetime import datetime
from serpapi import GoogleSearch
import os
import random
import requests

from config import HEADERS, JSONBIN_URL

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')

@busqueda_bp.route('/index')
def  index():
    return render_template('busqueda/index.html')

@busqueda_bp.route('/indexUsuarioAdministrador')
def  indexUsuarioAdministrador():
    return render_template('busqueda/indexUsuarioAdministrador.html')

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
    

@busqueda_bp.route('/buscarVuelo')
def buscarVuelo():
    API_KEY = 'feea122bafbb43aa26a1e19e957c5a558392c4be1d498f7c8b89a7d911648c5b'
    url = 'https://serpapi.com/search.json'

    departure_airports = ['PEK', 'LAX', 'JFK', 'ORD', 'SFO']
    arrival_airports = ['AUS', 'DFW', 'ATL', 'SEA', 'DEN']

    departure_id = random.choice(departure_airports)
    arrival_id = random.choice(arrival_airports)

    params = {
        'engine': 'google_flights',
        'departure_id': departure_id, 
        'arrival_id': arrival_id,    
        'outbound_date': '2024-10-26',
        'return_date': '2024-11-01',
        'currency': 'USD',
        'hl': 'en',
        'api_key': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        best_flights = data.get('best_flights', [])
        return render_template('buscarVuelo.html', best_flights=best_flights, departure_id=departure_id, arrival_id=arrival_id)
    else:
        error_message = f'Error: {response.status_code} - {response.text}'
        return render_template('busqueda/buscarVuelo.html', error=error_message)

@busqueda_bp.route('/buscarHotel')
def buscarHotel():
    API_KEY = 'feea122bafbb43aa26a1e19e957c5a558392c4be1d498f7c8b89a7d911648c5b'
    url = "https://serpapi.com/search.json?engine=google_hotels&q=Bali+Resorts&check_in_date=2024-10-29&check_out_date=2024-10-30&adults=2&currency=USD&gl=us&hl=en"

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
    SERPAPI_API_KEY = os.getenv("feea122bafbb43aa26a1e19e957c5a558392c4be1d498f7c8b89a7d911648c5b") 

    params_vuelos = {
        "engine": "google_flights",
        "departure_id": "CDG",
        "arrival_id": "AUS",
        "outbound_date": "2024-10-26",
        "return_date": "2024-11-01",
        "currency": "EUR",
        "hl": "en",
        "api_key": SERPAPI_API_KEY
    }

    search_vuelos = GoogleSearch(params_vuelos)
    resultados_vuelos = search_vuelos.get_dict()

    # Manejar resultados de vuelos
    vuelos = resultados_vuelos.get("flights", [])
    precios_aleatorios = []
    price_insights = resultados_vuelos.get("price_insights", {})

    if vuelos:
        precios_aleatorios = random.sample([vuelo['price'] for vuelo in vuelos], min(3, len(vuelos)))
    else:
        precios_aleatorios = []

    return render_template(
        'busqueda/buscar_Precios_de_Vuelos.html',
        precios=precios_aleatorios,
        price_insights=price_insights
)

@busqueda_bp.app_template_filter('to_datetime')
def to_datetime(value):
    return datetime.strptime(value, '%Y-%m-%d')

@busqueda_bp.route('/buscar_Precios_de_Hoteles')
def buscar_Precios_de_Hoteles():
    API_KEY = 'feea122bafbb43aa26a1e19e957c5a558392c4be1d498f7c8b89a7d911648c5b'
    url = 'https://serpapi.com/search.json'

    params = {
        "engine": "google_hotels",
        "q": "Bali Resorts",
        "check_in_date": "2024-10-26",
        "check_out_date": "2024-10-27",
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