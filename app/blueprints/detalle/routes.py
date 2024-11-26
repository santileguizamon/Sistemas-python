from flask import Blueprint, render_template,url_for,request,redirect
from flask import Flask, jsonify
from datetime import datetime
#from serpapi import GoogleSearch
import os
import random
import requests

from config import HEADERS, JSONBIN_URL

detalle_bp = Blueprint('detalle',__name__,url_prefix='/detalle')

@detalle_bp.route('/compraVuelo/<int:vuelo_id>', methods=['GET'])
def compraVuelo(vuelo_id):

    conexion = conectar()
    cursor = conexion.cursor()

    query = '''
    SELECT v.id, v.origen, v.destino, v.fecha_salida, v.horario_salida, v.horario_llegada, v.precio
    FROM vuelos v
    WHERE v.id = ?
    '''
    cursor.execute(query, (vuelo_id,))
    vuelo = cursor.fetchone()

    conexion.close()

    if not vuelo:
        return render_template('detalle/error.html', mensaje="El vuelo no existe o ya no está disponible.")

    return render_template('detalle/compraVuelo.html', vuelo=vuelo)

@detalle_bp.route('/detalleHotel/<int:hotel_id>', methods=['GET'])
def detalleHotel(hotel_id):

    conexion = conectar()
    cursor = conexion.cursor()

    query = '''
    SELECT h.id, h.nombre, h.lugar, h.descripcion, h.precio_por_noche, h.habitaciones_disponibles, h.imagen
    FROM hoteles h
    WHERE h.id = ?
    '''
    cursor.execute(query, (hotel_id,))
    hotel = cursor.fetchone()

    conexion.close()

    if not hotel:
        return render_template('detalle/error.html', mensaje="El hotel no existe o ya no está disponible.")

    return render_template('detalle/detalleHotel.html', hotel=hotel)

@detalle_bp.route('/users')
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
        'celular': user['cell']

    }
    return render_template("detalle/usuarios.html" , infoPersona =infoPersona )
    
@detalle_bp.route('/users/information')
def usersInformation():
    response = requests.get('https://randomuser.me/api/')
    data = response.json()
    return jsonify({"data" : data['results'][0]}), 200

@detalle_bp.route('/Lista_de_Usuarios')
def Lista_de_Usuarios():
    return render_template('detalle/Lista_de_Usuarios.html')

@detalle_bp.route('/Vuelos')
def Vuelos():
    return render_template('detalle/Vuelos.html')

@detalle_bp.route('/Hoteles')
def Hoteles():
    return render_template('detalle/Hoteles.html')

@detalle_bp.route('/Precios_de_Vuelos')
def Precios_de_Vuelos():
    return render_template('detalle/Precios_de_Vuelos.html')

@detalle_bp.route('/Precios_de_Hoteles')
def Precios_de_Hoteles():
    return render_template('detalle/Precios_de_Hoteles.html')
    


