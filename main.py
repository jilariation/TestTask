import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.config import settings
from src.app.core.logging import logger
from src.app.task.controller import router as tasks_router
import time


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.4f}s"
        )

        return response

    app.include_router(tasks_router)

    @app.get("/", tags=["health"])
    async def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_TITLE} v{settings.APP_VERSION}")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)