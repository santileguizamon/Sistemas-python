from flask import Flask, render_template
from app.blueprints.auth import auth_bp
from app.blueprints.busqueda import busqueda_bp
from app.blueprints.detalle import detalle_bp

def create_app():
    app=Flask(__name__)

    app.config['SECRET KEY']= 'asas'

    app.register_blueprint(auth_bp)
    app.register_blueprint(busqueda_bp)
    app.register_blueprint(detalle_bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
