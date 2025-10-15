from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import health, ingest, query, data


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Vehicle Service RAG Assistant", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    app.include_router(health.router)
    app.include_router(ingest.router)
    app.include_router(query.router)
    app.include_router(data.router)

    return app


app = create_app()