import sqlite3
from app.db.conexion import conectar

def insertar_hoteles(conexion):
    cursor = conexion.cursor()

    hoteles = [
        ('Capella Bangkok', 'Un hotel elegante en Tailandia', 100),
        ('Passalacqua', 'El mejor hotel de Italia', 100),
        ('Rosewood', 'El hotel Rosewood Hong Kong Hotel, de 5 estrellas, está situado en el barrio Kowloon de Hong Kong', 322),
        ('Cheval Blanc', 'En el hotel Cheval Blanc, vas a encontrar la paz y comodidad que precisas para tus vacaciones', 72)
    ]

    cursor.executemany('''
        INSERT INTO hoteles (nombre, descripcion, habitaciones)
        VALUES (?, ?, ?)
    ''', hoteles)

    conexion.commit()
    print("Datos de hoteles insertados correctamente.")

if __name__ == "__main__":

    conexion = conectar()
    
    insertar_hoteles(conexion)
    
    conexion.close()

