from app import create_app
from datetime import datetime
from app.db.conexion import conectar
from app.db.setup_db import crear_tablas
import os

def main():
    conexion = conectar()
    crear_tablas(conexion)

app = create_app()
app.secret_key = os.getenv("123", "una_clave_por_defecto")

@app.template_filter()
def to_datetime(timestamp):
    """Convert Unix timestamp to a readable date format."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

if __name__ == '__main__':
    main()
    app.run(debug=True)







     