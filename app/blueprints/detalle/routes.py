from flask import Blueprint, render_template,url_for,request,redirect
from flask import Flask, jsonify
from datetime import datetime
from serpapi import GoogleSearch
import os
import random
import requests

from config import HEADERS, JSONBIN_URL

detalle_bp = Blueprint('detalle',__name__,url_prefix='/detalle')

@detalle_bp.route('/compraVuelo')
def compraVuelo():
    return render_template('detalle/compraVuelo.html')

@detalle_bp.route('/detalleHotel')
def  detalleHotel():
    return render_template('detalle/detalleHotel')

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
    

