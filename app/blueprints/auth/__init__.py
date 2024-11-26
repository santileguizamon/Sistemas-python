from flask import Flask, flash, redirect, render_template, request, url_for
from app.blueprints.auth.routes import auth_bp
from app.blueprints.busqueda.routes import busqueda_bp
from app.blueprints.detalle.routes import detalle_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  
            login(user)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for('busqueda.index'))
        else:
            flash("Credenciales incorrectas.", "danger")
    return render_template('auth/logIn.html')

def create_app():
    app=Flask(__name__)

    app.config['SECRET KEY']= 'asas'

    app.register_blueprint(auth_bp)
    app.register_blueprint(busqueda_bp)
    app.register_blueprint(detalle_bp)

    

    return app
