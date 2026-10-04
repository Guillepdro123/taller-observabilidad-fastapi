# Taller de Observabilidad - Sistema Academico

Proyecto FastAPI preparado para el analisis de observabilidad y calidad, con
mecanismos reales de observabilidad agregados (observabilidad.py): registro
de eventos y manejo/registro de errores, sin modificar la logica original.

## Ejecucion

python -m pip install -r requirements.txt

python -m uvicorn main:app --reload

Swagger:
http://127.0.0.1:8000/docs

## Endpoints

- GET /estudiantes/
- GET /estudiantes/{id_estudiante}
- POST /estudiantes/

## Observabilidad

- logs/app.log registra fecha/hora, metodo, endpoint, codigo de respuesta,
  tiempo de respuesta y resultado de cada peticion, ademas del detalle de
  cada error (datos invalidos, base de datos, API externa, excepciones).
- generar_trafico_logs.py genera trafico real de prueba (casos validos e
  invalidos) contra el servidor en ejecucion.
- benchmark_rendimiento.py mide tiempos reales (minimo, maximo, promedio)
  de los endpoints principales.

## Proposito academico

La aplicacion contiene situaciones deliberadas que deben ser investigadas
mediante pruebas controladas.

NO se proporciona una lista de los problemas. El estudiante debe
encontrarlos, demostrar cada hallazgo con evidencia, explicar su posible
causa e impacto y proponer una mejora tecnica.

No subir credenciales, tokens, claves API ni contrasenas.
