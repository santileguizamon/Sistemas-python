from app import create_app
from datetime import datetime
from app.db.conexion import conectar
from app.db.setup_db import crear_tablas

app = create_app()

def main():
    conexion = conectar()
    crear_tablas(conexion)

def my_custom_filter(value):
    return value  

@app.template_filter()
def to_datetime(timestamp):
    """Convert Unix timestamp to a readable date format."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

if __name__ == '__main__':
    app.run(debug=True)







     