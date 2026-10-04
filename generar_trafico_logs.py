# -*- coding: utf-8 -*-
"""
Genera trafico HTTP real contra el Sistema Academico (debe estar
corriendo en http://127.0.0.1:8000, por ejemplo ejecutando main.py en
otra terminal) para producir evidencia real de los mecanismos de
observabilidad (logs/app.log), cubriendo los escenarios pedidos en la
guia del taller (datos validos, datos invalidos, campos faltantes,
valores fuera de rango, id existente, id inexistente, comportamiento
del servicio externo y un error real de base de datos).

No modifica el proyecto original: solo lo consume como cliente HTTP /
como segunda conexion sqlite para forzar el bloqueo en el caso 7.
"""
import sqlite3
import time

import requests

BASE_URL = "http://127.0.0.1:8000"
DB = "academico.db"


def paso(titulo):
    print("\n" + "=" * 78)
    print(titulo)
    print("=" * 78)


def caso_1_datos_validos():
    paso("CASO 1: Datos válidos — POST /estudiantes/")
    r = requests.post(f"{BASE_URL}/estudiantes/", json={
        "nombre": "Camila Pérez",
        "programa": "Ingeniería de Sistemas",
        "semestre": 4,
        "promedio": 4.1,
    }, timeout=15)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text[:300])


def caso_2_datos_invalidos_tipo():
    paso("CASO 2: Datos inválidos (tipo incorrecto) — semestre = \"no-es-un-número\"")
    r = requests.post(f"{BASE_URL}/estudiantes/", json={
        "nombre": "Dato Inválido",
        "programa": "Ingeniería de Sistemas",
        "semestre": "no-es-un-número",
        "promedio": 4.0,
    }, timeout=10)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text)


def caso_3_campo_faltante():
    paso("CASO 3: Campo faltante — sin el campo \"promedio\"")
    r = requests.post(f"{BASE_URL}/estudiantes/", json={
        "nombre": "Sin Promedio",
        "programa": "Ingeniería de Sistemas",
        "semestre": 2,
    }, timeout=10)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text)


def caso_4_valor_fuera_de_rango():
    paso("CASO 4: Valor fuera de rango (aceptado por el modelo actual) — semestre=999, promedio=11.7")
    r = requests.post(f"{BASE_URL}/estudiantes/", json={
        "nombre": "Fuera De Rango",
        "programa": "Ingeniería de Sistemas",
        "semestre": 999,
        "promedio": 11.7,
    }, timeout=15)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text[:300])


def caso_5_id_existente():
    paso("CASO 5: Identificador existente — GET /estudiantes/1")
    r = requests.get(f"{BASE_URL}/estudiantes/1", timeout=10)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text)


def caso_6_id_inexistente():
    paso("CASO 6: Identificador inexistente — GET /estudiantes/999999")
    r = requests.get(f"{BASE_URL}/estudiantes/999999", timeout=10)
    print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text)


def caso_7_error_base_datos():
    paso("CASO 7: Error real de base de datos — academico.db bloqueada por otra conexión")
    bloqueador = sqlite3.connect(DB, timeout=1)
    bloqueador.execute("BEGIN EXCLUSIVE")
    try:
        r = requests.post(f"{BASE_URL}/estudiantes/", json={
            "nombre": "Prueba BD Bloqueada",
            "programa": "Ingeniería de Sistemas",
            "semestre": 2,
            "promedio": 3.5,
        }, timeout=10)
        print("Código de respuesta:", r.status_code, "| Cuerpo:", r.text)
    finally:
        bloqueador.rollback()
        bloqueador.close()


if __name__ == "__main__":
    caso_1_datos_validos()
    time.sleep(0.3)
    caso_2_datos_invalidos_tipo()
    time.sleep(0.3)
    caso_3_campo_faltante()
    time.sleep(0.3)
    caso_4_valor_fuera_de_rango()
    time.sleep(0.3)
    caso_5_id_existente()
    time.sleep(0.3)
    caso_6_id_inexistente()
    time.sleep(0.3)
    caso_7_error_base_datos()

    print("\n\nTráfico generado (7 escenarios). Revise logs/app.log para ver los registros.")
