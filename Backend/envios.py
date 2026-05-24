# Backend/envios.py
import sqlite3

class EnvioDB:

    def __init__(self, db_name):
        self.db_name = db_name

    # ==========================================================================
    # CONEXIÓN A LA BASE DE DATOS
    # ==========================================================================
    def conectar(self):
        return sqlite3.connect(self.db_name)

    # ==========================================================================
    # CREAR TABLAS (ESTRUCTURA DEL MODELO ESTRELLA)
    # ==========================================================================
    def crear_tabla(self):
        conn = self.conectar()
        cursor = conn.cursor()

        # 1. TABLA CLIENTES (DIMENSIÓN 1)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL
        )
        """)

        # 2. TABLA DESTINOS (DIMENSIÓN 2) - ¡ESTA ES LA QUE ASEGURA TU ESTRELLA!
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinos (
            destino TEXT PRIMARY KEY,
            region TEXT NOT NULL
        )
        """)

        # 3. TABLA ENVIOS (TABLA DE HECHOS CENTRAL)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            peso REAL,
            destino TEXT,
            tipo TEXT,
            costo REAL,
            fecha TEXT,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY(destino) REFERENCES destinos(destino)
        )
        """)

        conn.commit()
        conn.close()

    # ==========================================================================
    # OPERACIÓN CRUD: CREATE / INSERTAR
    # ==========================================================================
    def insertar(self, id_cliente, peso, destino, tipo, costo, fecha):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO envios (id_cliente, peso, destino, tipo, costo, fecha)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (id_cliente, peso, destino, tipo, costo, fecha))
        conn.commit()
        conn.close()

    # ==========================================================================
    # OPERACIÓN CRUD: READ / CONSULTAR (CON JOINS PARA REPORTES)
    # ==========================================================================
    def consultar(self):
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Unimos las 3 tablas relacionales para mostrar un manifiesto limpio en consola
        cursor.execute("""
        SELECT 
            envios.id,
            clientes.nombre,
            envios.peso,
            envios.destino,
            destinos.region,
            envios.tipo,
            envios.costo,
            envios.fecha
        FROM envios
        LEFT JOIN clientes ON envios.id_cliente = clientes.id_cliente
        LEFT JOIN destinos ON envios.destino = destinos.destino
        ORDER BY envios.id ASC
        """)

        datos = cursor.fetchall()
        conn.close()
        return datos

    # ==========================================================================
    # OPERACIÓN CRUD: UPDATE / ACTUALIZAR
    # ==========================================================================
    def actualizar(self, id_envio, nuevo_destino):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE envios
        SET destino = ?
        WHERE id = ?
        """, (nuevo_destino, id_envio))
        conn.commit()
        conn.close()

    # ==========================================================================
    # OPERACIÓN CRUD: DELETE / ELIMINAR
    # ==========================================================================
    def eliminar(self, id_envio):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM envios
        WHERE id = ?
        """, (id_envio,))
        conn.commit()
        conn.close()