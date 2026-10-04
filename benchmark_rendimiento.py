# -*- coding: utf-8 -*-
"""
Script de medicion de rendimiento para el Analisis de rendimiento del
taller. Ejecuta N peticiones reales contra 3 endpoints del Sistema
Academico (debe estar corriendo en http://127.0.0.1:8000, por ejemplo
ejecutando main.py) y reporta tiempo minimo, maximo, promedio y codigo
de respuesta de cada uno.

No modifica el proyecto original: solo lo consume como cliente HTTP.
"""
import statistics
import time

import requests

BASE_URL = "http://127.0.0.1:8000"
N_PRUEBAS = 10

ENDPOINTS = [
    ("GET", "/estudiantes/", None),
    ("GET", "/estudiantes/1", None),
    ("POST", "/estudiantes/", {
        "nombre": "Prueba Rendimiento",
        "programa": "Ingeniería de Sistemas",
        "semestre": 3,
        "promedio": 4.0,
    }),
]


def medir(metodo, ruta, cuerpo):
    tiempos = []
    codigo = None
    for _ in range(N_PRUEBAS):
        inicio = time.perf_counter()
        try:
            if metodo == "GET":
                resp = requests.get(BASE_URL + ruta, timeout=15)
            else:
                resp = requests.post(BASE_URL + ruta, json=cuerpo, timeout=15)
            codigo = resp.status_code
        except requests.exceptions.RequestException as exc:
            codigo = f"ERROR: {exc.__class__.__name__}"
        duracion = time.perf_counter() - inicio
        tiempos.append(duracion)
    return tiempos, codigo


def main():
    print(f"{'Endpoint':35} {'Método':7} {'Pruebas':8} {'Mín(s)':8} {'Máx(s)':8} {'Prom(s)':8} {'Código'}")
    print("-" * 95)
    resultados = []
    for metodo, ruta, cuerpo in ENDPOINTS:
        tiempos, codigo = medir(metodo, ruta, cuerpo)
        minimo, maximo, promedio = min(tiempos), max(tiempos), statistics.mean(tiempos)
        resultados.append((ruta, metodo, len(tiempos), minimo, maximo, promedio, codigo))
        print(f"{ruta:35} {metodo:7} {len(tiempos):<8} {minimo:<8.4f} {maximo:<8.4f} {promedio:<8.4f} {codigo}")

    print("\nResumen:")
    peor = max(resultados, key=lambda r: r[5])
    print(f"Endpoint menos eficiente (mayor tiempo promedio): {peor[1]} {peor[0]} "
          f"con {peor[5]:.4f} s en promedio.")


if __name__ == "__main__":
    main()
