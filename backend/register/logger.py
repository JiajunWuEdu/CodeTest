from fastapi import FastAPI, Request
import os
from loguru import logger

logger.add(
    os.path.join("logs", '{time:YYYY-MM-DD_HH-mm-ss}.log'),
    encoding='utf-8',
    level='INFO'
)


def register_logger(app: FastAPI):
    @app.middleware("http")
    async def add_logger_middleware(request: Request, call_next):
        if not hasattr(request.state, "logger"):
            request.state.logger = logger
        request.state.logger.info(f"IP:{request.client.host}-method:{request.method}-url:{request.url}")
        response = await call_next(request)
        return response
