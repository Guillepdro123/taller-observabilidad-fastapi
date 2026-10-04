import sqlite3

DB = "academico.db"

def inicializar():
    conexion = sqlite3.connect(DB)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            programa TEXT NOT NULL,
            semestre INTEGER NOT NULL,
            promedio REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def listar():
    conexion = sqlite3.connect(DB)
    datos = conexion.execute(
        "SELECT id, nombre, programa, semestre, promedio FROM estudiantes"
    ).fetchall()
    conexion.close()
    return datos

def buscar(id_estudiante):
    conexion = sqlite3.connect(DB)
    dato = conexion.execute(
        "SELECT id, nombre, programa, semestre, promedio "
        "FROM estudiantes WHERE id = ?", (id_estudiante,)
    ).fetchone()
    conexion.close()
    return dato

def guardar(estudiante):
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO estudiantes(nombre, programa, semestre, promedio) "
        "VALUES (?, ?, ?, ?)",
        (estudiante.nombre, estudiante.programa,
         estudiante.semestre, estudiante.promedio)
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()
    return nuevo_id
