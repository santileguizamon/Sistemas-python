from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for('auth.login'))
        if current_user.rol != 'admin':
            flash("No tienes permiso para acceder a esta página.", "danger")
            return redirect(url_for('busqueda.index'))
        return f(*args, **kwargs)
    return decorated_function
