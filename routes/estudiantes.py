from fastapi import APIRouter
from models.estudiante import Estudiante
from services.estudiante_service import (
    obtener_estudiantes, obtener_estudiante, registrar_estudiante
)

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("/")
def listar_estudiantes():
    return obtener_estudiantes()

@router.get("/{id_estudiante}")
def consultar_estudiante(id_estudiante: int):
    estudiante = obtener_estudiante(id_estudiante)

    # Situación intencional para investigar: revisar el código HTTP.
    if not estudiante:
        return {"mensaje": "Estudiante no encontrado"}

    return estudiante

@router.post("/")
def crear_estudiante(estudiante: Estudiante):
    return registrar_estudiante(estudiante)
