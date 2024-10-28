from flask import Blueprint, render_template,url_for,request,redirect,jsonify
import requests

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')

params = {
  'access_key': 'ab4cb3a8be3f01ec3ad753e67407d71f'
}
headers = {
	"x-rapidapi-key": "Sign Up for Key",
	"x-rapidapi-host": "agoda-com.p.rapidapi.com"
}

@busqueda_bp.route('/index')
def  index():
    return render_template('busqueda/index.html')

@busqueda_bp.route('/indexHotel')
def   indexHotel():
    return render_template('busqueda/indexHotel.html')

busqueda_bp.route('/buscadorVuelo')
def  buscadorVuelo():
     return render_template('busqueda/buscadorVuelo.html')


@busqueda_bp.route('/buscadorVuelo',methods=['GET','POST'])
def buscadorVueloSection():
    if request.method == 'POST':
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        fecha_ida = request.form.get('fecha-ida')
        fecha_vuelta = request.form.get('fecha-vuelta')
        pasajeros = request.form.get('pasajeros')

    try:
        api_result = requests.get('https://api.aviationstack.com/v1/flights', params)
        api_result.raise_for_status()
        data = api_result.json()
    
        vuelos_info = []
        for vuelo in data['data']:  
            vuelo_info = {
                'nombre': vuelo.get('flight', {}).get('iata'),  
                'horario_salida': vuelo.get('departure', {}).get('estimated'),
                'fecha ': vuelo.get('departure', {}).get('scheduled'),    
                'destino': vuelo.get('arrival', {}).get('iata'),  
                'origen': vuelo.get('departure', {}).get('iata'), 
                'horario_llegada': vuelo.get('arrival', {}).get('estimated')
            }
            vuelos_info.append(vuelo_info)
        
        return jsonify(vuelos_info)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


    

@busqueda_bp.route('/buscadorHotel', methods=['GET','POST'])
def buscadorHotel():
    if request.method == 'POST':
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        fecha_ida = request.form.get('fecha-ida')
        fecha_vuelta = request.form.get('fecha-vuelta')

    try:
        response = requests.get('', headers)
        api_respuesta =  response.json()
        data = api_respuesta.json()
    
        hoteles_info = []
        for hotel in data['data']:  
            hotel_info = {
                'nombre': hotel.get('hotelName', {}).get('hotelName'),  
                'fecha ': hotel.get('departure', {}).get('Check-in date'),    
                'pasajeros': hotel.get('pasajeros', {}).get('pasajeros'),  
            }
            hoteles_info.append(hotel_info)
        
        return jsonify(hotel_info)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
