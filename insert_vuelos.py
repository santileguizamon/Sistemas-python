import sqlite3
from app.db.conexion import conectar

def insertar_vuelos(conexion):
    cursor = conexion.cursor()

    vuelos = [
        ('Buenos Aires', 'Madrid', '2024-12-01', '2024-12-15', '2024-12-01 10:00:00', '2024-12-01 22:00:00', 200),
        ('Madrid', 'Barcelona', '2024-12-10', '2024-12-12', '2024-12-10 08:00:00', '2024-12-10 09:15:00', 150),
        ('Barcelona', 'Buenos Aires', '2024-12-20', '2024-12-30', '2024-12-20 18:00:00', '2024-12-21 08:00:00', 180)
    ]
    
    cursor.executemany('''
        INSERT INTO vuelos (origen, destino, fecha_ida, fecha_vuelta, horario_salida, horario_llegada, pasajeros)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', vuelos)

    conexion.commit()

    print("Datos de vuelos insertados correctamente.")

if __name__ == "__main__":
   
    conexion = conectar()
    
    insertar_vuelos(conexion)
    
    conexion.close()
