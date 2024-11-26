import sqlite3
from app.db.conexion import conectar

def insertar_vuelos(conexion):
    cursor = conexion.cursor()

    lugares = [
        ('Buenos Aires'),
        ('Madrid'),
        ('Barcelona'),
        ('Hong Kong'),
        ('Mexico'),
        ('Tailandia'),
    ]
    
    cursor.executemany('''
        INSERT INTO lugares (destino)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', lugares)

    conexion.commit()

    print("Datos de lugares insertados correctamente.")

if __name__ == "__main__":
   
    conexion = conectar()
    
    insertar_lugares(conexion)
    
    conexion.close()
