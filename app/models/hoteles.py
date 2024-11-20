def obtener_hoteles(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM hoteles')
    return cursor.fetchall()