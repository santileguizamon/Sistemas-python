from flask import Flask, Blueprint
from app.blueprints.auth.routes import auth_bp
from app.blueprints.busqueda.routes import busqueda_bp
from app.blueprints.detalle.routes import detalle_bp

busqueda_bp = Blueprint('busqueda',__name__,url_prefix='/busqueda')
from . import routes

def create_app():
    app=Flask(__name__)

    app.config['SECRET KEY']= 'asas'

    app.register_blueprint(auth_bp)
    app.register_blueprint(busqueda_bp)
    app.register_blueprint(detalle_bp)

    return app
