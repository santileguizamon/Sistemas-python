def obtener_vuelos(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM vuelos')
    return cursor.fetchall()