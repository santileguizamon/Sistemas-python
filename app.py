from flask import Flask, request, jsonify, render_template
from datetime import datetime
from serpapi import GoogleSearch
import os
import random
import requests

from config import HEADERS, JSONBIN_URL

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/users')
def users():
    response = requests.get('https://randomuser.me/api/')
    data = response.json()
    user = data['results'][0]

    infoPersona = {
        'name':  f"{user['name']['title']} {user['name']['first']} {user['name']['last']}",
        'gender': user['gender'],
        'street': f"{user['location']['street']['number']} {user ['location']['street']['name']}",
        'city': user['location']['city'],
        'state': user['location']['state'],
        'country': user['location']['country'],
        'email': user['email'],
        'celular': user['cell'],

    }
    return render_template("usuarios.html" , infoPersona =infoPersona )
    
@app.route('/users/information')
def usersInformation():
    response = requests.get('https://randomuser.me/api/')
    data = response.json()
    return jsonify({"data" : data['results'][0]}), 200

@app.route('/Lista_de_Usuarios')
def Lista_de_Usuarios():
    return render_template('Lista_de_Usuarios.html')

@app.route('/Vuelos')
def Vuelos():
    return render_template('Vuelos.html')

@app.route('/Hoteles')
def Hoteles():
    return render_template('Hoteles.html')

@app.route('/Precios_de_Vuelos')
def Precios_de_Vuelos():
    return render_template('Precios_de_Vuelos.html')

@app.route('/Precios_de_Hoteles')
def Precios_de_Hoteles():
    return render_template('Precios_de_Hoteles.html')


@app.route('/buscarVuelo')
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
        return render_template('buscarVuelo.html', error=error_message)

@app.route('/buscarHotel')
def buscarHotel():
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
    
    return render_template('buscarHotel.html', hotels=hotels)


SERPAPI_API_KEY = 'feea122bafbb43aa26a1e19e957c5a558392c4be1d498f7c8b89a7d911648c5b'

@app.route('/buscar_Precios_de_Vuelos')
def buscar_Precios_de_Vuelos():
    # Parámetros para la búsqueda de vuelos
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
        # Seleccionar precios aleatorios de los vuelos
        precios_aleatorios = random.sample([vuelo['price'] for vuelo in vuelos], min(3, len(vuelos)))
    else:
        precios_aleatorios = []

    return render_template(
        'buscar_precios_de_vuelos.html',
        precios=precios_aleatorios,
        price_insights=price_insights
    )

@app.template_filter()
def to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

@app.route('/buscar_Precios_de_Hoteles')
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
    
    return render_template('buscar_Precios_de_Hoteles.html', hotels=hotels)

if __name__ == '__main__':
    app.run(debug=True)