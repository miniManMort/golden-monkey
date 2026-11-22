"""FastAPI application setup, shared middleware, and frontend serving."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response

from . import database
from .errors import ApiError
from .routers import (
    character_classes,
    exports,
    health,
    monsters,
    rule_sections,
    spells,
)

logger = logging.getLogger(__name__)
DIST_DIR = Path(__file__).resolve().parents[1] / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    database.initialize_database()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title="Golden Monkey API", version="1.0.0", lifespan=lifespan)

    @application.middleware("http")
    async def limit_request_body(request: Request, call_next: Any) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                return JSONResponse(
                    status_code=400, content={"error": "Invalid Content-Length."}
                )
            if length > 1_000_000:
                return JSONResponse(
                    status_code=413, content={"error": "Request body is too large."}
                )
        return await call_next(request)

    @application.exception_handler(ApiError)
    async def handle_api_error(_: Request, error: ApiError) -> JSONResponse:
        return JSONResponse(status_code=error.status, content={"error": str(error)})

    @application.exception_handler(RequestValidationError)
    async def handle_request_validation(
        _: Request, error: RequestValidationError
    ) -> JSONResponse:
        if any(item.get("type") == "json_invalid" for item in error.errors()):
            message = "Request body must be valid JSON."
        else:
            message = "Request body must be a JSON object."
        return JSONResponse(status_code=400, content={"error": message})

    @application.exception_handler(HTTPException)
    async def handle_http_error(_: Request, error: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code, content={"error": str(error.detail)}
        )

    @application.exception_handler(sqlite3.IntegrityError)
    async def handle_integrity_error(
        _: Request, error: sqlite3.IntegrityError
    ) -> JSONResponse:
        if "UNIQUE constraint failed" in str(error):
            error_text = str(error)
            if "monster" in error_text:
                label = "monster"
            elif "character_class" in error_text:
                label = "character class"
            elif "rule_section" in error_text:
                label = "rule section"
            else:
                label = "spell"
            message = f"A {label} with that name already exists."
            return JSONResponse(status_code=409, content={"error": message})
        logger.error("Database integrity error: %s", error)
        return JSONResponse(
            status_code=500, content={"error": "The database rejected the operation."}
        )

    @application.exception_handler(sqlite3.Error)
    async def handle_database_error(_: Request, error: sqlite3.Error) -> JSONResponse:
        logger.error("Database operation failed: %s", error)
        return JSONResponse(
            status_code=500, content={"error": "The operation could not be completed."}
        )

    @application.exception_handler(OSError)
    async def handle_os_error(_: Request, error: OSError) -> JSONResponse:
        logger.error("File operation failed: %s", error)
        return JSONResponse(
            status_code=500, content={"error": "The operation could not be completed."}
        )

    application.include_router(health.router)
    application.include_router(monsters.router)
    application.include_router(spells.router)
    application.include_router(character_classes.router)
    application.include_router(character_classes.alias_router)
    application.include_router(rule_sections.router)
    application.include_router(rule_sections.alias_router)
    application.include_router(exports.router)

    def serve_frontend(request_path: str) -> Response:
        if request_path == "api" or request_path.startswith("api/"):
            raise ApiError(404, "API endpoint not found.")
        if not DIST_DIR.is_dir():
            message = (
                "The React frontend has not been built. Run `npm install` and `npm run build` "
                "from app-react."
            )
            return JSONResponse(status_code=503, content={"error": message})
        relative = request_path or "index.html"
        target = (DIST_DIR / relative).resolve()
        if not target.is_relative_to(DIST_DIR.resolve()) or not target.is_file():
            target = DIST_DIR / "index.html"
        if not target.is_file():
            raise ApiError(404, "Frontend entry point not found.")
        return FileResponse(target)

    @application.get("/")
    def serve_index() -> Response:
        return serve_frontend("")

    @application.get("/{request_path:path}")
    def serve_static_or_spa(request_path: str) -> Response:
        return serve_frontend(request_path)

    return application


app = create_app()
