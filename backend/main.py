"""Point d'entree de l'application FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.persistence.colis_model import ColisModel  # noqa: F401
from src.interfaces.api.routes.colis_routes import router as colis_router
from src.shared.config import settings


def create_app() -> FastAPI:
    """Factory de l'application FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(colis_router)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
        }

    @app.on_event("startup")
    def on_startup() -> None:
        """Creer les tables au demarrage (lecture dynamique de engine)."""
        # Import dynamique pour que le monkey-patch des tests soit pris en compte
        from src.infrastructure.persistence import database as db_module
        from src.infrastructure.persistence import Base
        Base.metadata.create_all(bind=db_module.engine)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
