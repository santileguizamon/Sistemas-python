def crear_tablas(conexion):
    cursor = conexion.cursor()

    # Crear tablas
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
        nombre_avion TEXT NOT NULL,
        origen_id INTEGER NOT NULL,
        destino_id INTEGER NOT NULL,
        horario_salida DATETIME NOT NULL,
        horario_llegada DATETIME NOT NULL,
        precio DECIMAL NOT NULL,
        FOREIGN KEY (origen_id) REFERENCES lugares (id),
        FOREIGN KEY (destino_id) REFERENCES lugares (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hoteles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        lugar_id INTEGER NOT NULL,
        descripcion TEXT,
        imagenes IMG,
        habitaciones INTEGER NOT NULL,
        FOREIGN KEY (lugar_id) REFERENCES lugares (id)
    )
    ''')

    conexion.commit()

def insertar_datos(conexion):
    cursor = conexion.cursor()


    lugares = [
        ('Buenos Aires', 'origen'),
        ('Madrid', 'destino'),
        ('Barcelona', 'destino')
    ]
    cursor.executemany('INSERT INTO lugares (nombre, tipo) VALUES (?, ?)', lugares)

    conexion.commit()