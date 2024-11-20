def obtener_lugares(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM lugares')
    return cursor.fetchall()