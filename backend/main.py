"""Point d'entree de l'application FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.persistence.colis_model import ColisModel  # noqa: F401
from src.infrastructure.persistence.historique_model import HistoriqueStatutModel  # noqa: F401
from src.infrastructure.persistence.livreur_model import LivreurModel  # noqa: F401
from src.interfaces.api.routes.colis_routes import router as colis_router
from src.interfaces.api.routes.livreurs_routes import router as livreurs_router
from src.interfaces.api.routes.routage_routes import router as routage_router
from src.shared.config import settings


def create_app() -> FastAPI:
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
    app.include_router(livreurs_router)
    app.include_router(routage_router)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
        }

    @app.on_event("startup")
    def on_startup() -> None:
        from src.infrastructure.persistence import database as db_module
        from src.infrastructure.persistence import Base
        Base.metadata.create_all(bind=db_module.engine)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
