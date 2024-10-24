from flask import Blueprint, render_template,url_for,request,redirect

detalle_bp = Blueprint('detalle',__name__,url_prefix='/detalle')

@detalle_bp.route('/compraVuelo')
def compraVuelo():
    return render_template('detalle/compraVuelo.html')

@detalle_bp.route('/detalleHotel')
def  detalleHotel():
    return render_template('detalle/detalleHotel')
