from app.db.conexion import conectar

def crear_tablas(conexion):
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lugares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('origen', 'destino')) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vuelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT,
        destino TEXT,
        fecha_ida DATE,
        fecha_vuelta DATE,
        horario_salida DATETIME,
        horario_llegada DATETIME,
        pasajeros INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hoteles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        lugar_id INTEGER NOT NULL,
        descripcion TEXT,
        habitaciones INTEGER NOT NULL,
        FOREIGN KEY (lugar_id) REFERENCES lugares (id)
    )
    ''')

    conexion.commit()


if __name__ == "__main__":
    conexion = conectar()
    crear_tablas(conexion)
    print("Base de datos configurada con éxito.")
    conexion.close()