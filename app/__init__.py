from flask import Flask, render_template
from app.blueprints.auth.routes import auth_bp
from app.blueprints.busqueda.routes import busqueda_bp
from app.blueprints.detalle.routes import detalle_bp
from models.user import User

def create_app():
    app=Flask(__name__)

    app.config['SECRET KEY']= 'asas'

    app.register_blueprint(auth_bp)
    app.register_blueprint(busqueda_bp)
    app.register_blueprint(detalle_bp)

    app.init_app(app)
    login_manager = login_manager()
    login_manager.login_view = 'auth.logIn'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(busqueda_bp, url_prefix='/busqueda')
    app.register_blueprint(auth_bp, url_prefix='/auth.signIn')

    @app.route('/index')
    def index():
        return render_template('busqueda/index.html')
    
    return app


