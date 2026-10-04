from fastapi.testclient import TestClient
from main import app
from repositories.estudiante_repository import inicializar

client = TestClient(app)
inicializar()


# ---- Operaciones exitosas ----

def test_listar_estudiantes():
    respuesta = client.get("/estudiantes/")
    assert respuesta.status_code == 200


def test_crear_estudiante():
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Ana",
        "programa": "Ingeniería de Sistemas",
        "semestre": 5,
        "promedio": 4.2
    })
    assert respuesta.status_code == 200


# ---- Recursos inexistentes ----

def test_estudiante_inexistente():
    respuesta = client.get("/estudiantes/99999")
    assert respuesta.status_code == 404


# ---- Validación: datos inválidos / campos faltantes ----

def test_crear_estudiante_tipo_invalido():
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Dato Inválido",
        "programa": "Ingeniería de Sistemas",
        "semestre": "no-es-un-número",
        "promedio": 4.0
    })
    assert respuesta.status_code == 422


def test_crear_estudiante_campo_faltante():
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Sin Promedio",
        "programa": "Ingeniería de Sistemas",
        "semestre": 2
    })
    assert respuesta.status_code == 422


def test_crear_estudiante_valores_fuera_de_rango_no_se_rechazan():
    """El modelo actual no valida rangos (ver Error 6 del informe de
    auditoría): este caso documenta ese comportamiento, no lo corrige."""
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Fuera De Rango",
        "programa": "Ingeniería de Sistemas",
        "semestre": 999,
        "promedio": 11.7
    })
    assert respuesta.status_code == 200


# ---- Servicio externo ----

def test_registro_incluye_informacion_externa_o_falla_con_claridad():
    """La llamada a la API externa puede fallar según la red disponible
    (ver Errores 3-5 del informe); en ambos casos debe haber una
    respuesta, nunca un cuelgue indefinido gracias al observabilidad
    agregada (manejador de errores de API externa)."""
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Prueba Externa",
        "programa": "Ingeniería de Sistemas",
        "semestre": 3,
        "promedio": 4.0
    })
    assert respuesta.status_code in (200, 502)
