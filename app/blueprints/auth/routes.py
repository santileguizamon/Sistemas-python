from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        if email == 'usuario@example.com' and contraseña == 'contraseña123':
            return redirect(url_for('busqueda.index')) 
        else:
            return render_template('auth/signIn.html', error="Credenciales incorrectas")

    return render_template('auth/signIn.html')

@auth_bp.route('/signUp', methods=['POST', 'GET'])
def signUp():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')

        return redirect(url_for('auth.signIn'))

    return render_template('auth/signUp.html')
