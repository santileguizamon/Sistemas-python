from flask import Blueprint, render_template,url_for,request,redirect

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

@auth_bp.route('/signIn')
def  signIn():
    return render_template('auth/signIn.html')

@auth_bp.route('submit', methods=['Post'], endpoint= 'submit_auth' )
def submit():
    email =  request.form.get('email')
    contraseña = request.form.get('contraseña')
    return redirect(url_for('busqueda/index'))


@auth_bp.route('/signUp')
def signUp():
    return render_template('auth/signUp.html')

@auth_bp.route('another_submit', methods=['POST'], endpoint= 'submit_another')
def another_submit():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    contraseña = request.form.get('contraseña')
    rol = request.form.get('rol')
    return redirect (url_for('signIn'))