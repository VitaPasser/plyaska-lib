import logging
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def include_exceptions(app: FastAPI) -> FastAPI:
    app.add_exception_handler(Exception, unhandled_exception_handler)  # type: ignore
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(ValidationError, validation_exception_handler)  # type: ignore
    return app


async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail} on path {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    logging.error(f"HTTP Exception: 422 - {exc.errors()} on path {request.url.path}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"Unhandled Exception: {exc} "
        f"on path {request.url.path}\n{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
