from fastapi import FastAPI
from routes.estudiantes import router
from observabilidad import configurar_observabilidad

app = FastAPI(title="Sistema Académico - Taller de Observabilidad")
app.include_router(router)

# Mecanismos de observabilidad (registro de eventos + manejo/registro de
# errores). No modifica la lógica original de las rutas ni corrige los
# errores ya documentados en el informe de auditoría.
configurar_observabilidad(app)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema académico activo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
