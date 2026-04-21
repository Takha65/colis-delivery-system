from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """Verification de sante de l'application."""
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
