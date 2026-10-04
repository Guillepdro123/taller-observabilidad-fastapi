import requests
from repositories.estudiante_repository import guardar, listar, buscar

def consultar_api_externa(programa):
    # Situación intencional para investigar: no se configura timeout.
    respuesta = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        params={"company": programa}
    )
    return respuesta.json()

def obtener_estudiantes():
    return listar()

def obtener_estudiante(id_estudiante):
    return buscar(id_estudiante)

def registrar_estudiante(estudiante):
    nuevo_id = guardar(estudiante)
    informacion = consultar_api_externa(estudiante.programa)
    return {
        "id": nuevo_id,
        "estudiante": estudiante,
        "informacion_externa": informacion
    }
