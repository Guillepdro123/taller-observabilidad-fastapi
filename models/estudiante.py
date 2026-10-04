from pydantic import BaseModel

class Estudiante(BaseModel):
    nombre: str
    programa: str
    semestre: int
    promedio: float
