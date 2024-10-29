from flask import Blueprint, render_template,url_for,request,redirect

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        email =  request.form.get('email')
        contraseña = request.form.get('contraseña')
        return redirect(url_for('busqueda/index'))
    return render_template('auth/signIn.html')



@auth_bp.route('/signUp', methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')  
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')  
        rol = request.form.get('rol')  
        
        
        return redirect(url_for('auth/signIn.html'))

    return render_template('auth/signUp.html')