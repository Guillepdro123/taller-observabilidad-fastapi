# -*- coding: utf-8 -*-
"""
Modulo de observabilidad para el Sistema Academico.

Este modulo agrega mecanismos de observabilidad (registro de eventos y
manejo/registro de errores) SIN modificar la logica de negocio original
del proyecto (main.py, routes/, services/, repositories/, models/).
Los 8 errores ya identificados en el informe de auditoria se mantienen
intactos: lo que cambia es que ahora quedan registrados en el log en
lugar de pasar inadvertidos.

Se integra en main.py agregando:
    from observabilidad import configurar_observabilidad
    configurar_observabilidad(app)
"""
import logging
import os
import sqlite3
import time

import requests
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("sistema_academico")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formato = logging.Formatter(
        "%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    manejador_archivo = logging.FileHandler("logs/app.log", encoding="utf-8")
    manejador_archivo.setFormatter(formato)
    logger.addHandler(manejador_archivo)

    manejador_consola = logging.StreamHandler()
    manejador_consola.setFormatter(formato)
    logger.addHandler(manejador_consola)


def configurar_observabilidad(app):
    """Agrega el middleware de registro de eventos y los manejadores de
    errores a una instancia de FastAPI ya creada, sin tocar sus rutas."""

    @app.middleware("http")
    async def registrar_eventos(request: Request, call_next):
        """Registro de eventos: fecha/hora, metodo, endpoint, codigo de
        respuesta, tiempo de respuesta y resultado de la operacion."""
        inicio = time.time()
        try:
            respuesta = await call_next(request)
        except Exception:
            # Si la excepcion no fue capturada por los manejadores de abajo,
            # igual queda registrada aqui antes de propagarse.
            duracion = time.time() - inicio
            logger.info(
                "%s %s | ERROR (excepcion no controlada) | Tiempo: %.3fs",
                request.method, request.url.path, duracion
            )
            raise

        duracion = time.time() - inicio
        resultado = "Operación exitosa" if respuesta.status_code < 400 else "Error"
        logger.info(
            "%s %s | %s | Tiempo: %.3fs | %s",
            request.method, request.url.path, respuesta.status_code,
            duracion, resultado
        )
        return respuesta

    @app.exception_handler(RequestValidationError)
    async def manejar_datos_invalidos(request: Request, exc: RequestValidationError):
        logger.info(
            "%s %s | 422 | Error | Datos inválidos: %s",
            request.method, request.url.path, exc.errors()
        )
        return JSONResponse(
            status_code=422,
            content={"detalle": "Datos inválidos", "errores": exc.errors()},
        )

    @app.exception_handler(sqlite3.Error)
    async def manejar_error_base_datos(request: Request, exc: sqlite3.Error):
        logger.info(
            "%s %s | 500 | Error | Error de base de datos: %s",
            request.method, request.url.path, str(exc)
        )
        return JSONResponse(
            status_code=500,
            content={"detalle": "Error interno de base de datos"},
        )

    @app.exception_handler(requests.exceptions.RequestException)
    async def manejar_error_api_externa(request: Request, exc: requests.exceptions.RequestException):
        logger.info(
            "%s %s | 502 | Error | Error de comunicación con API externa: %s",
            request.method, request.url.path, str(exc)
        )
        return JSONResponse(
            status_code=502,
            content={"detalle": "Error de comunicación con el servicio externo"},
        )

    @app.exception_handler(Exception)
    async def manejar_excepcion_inesperada(request: Request, exc: Exception):
        logger.info(
            "%s %s | 500 | Error | Excepción inesperada: %s: %s",
            request.method, request.url.path, type(exc).__name__, str(exc)
        )
        return JSONResponse(
            status_code=500,
            content={"detalle": "Error interno inesperado"},
        )

    return app
