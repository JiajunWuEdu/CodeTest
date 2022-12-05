import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def all_exception_handler(request: Request, e: HTTPException):
        request.state.logger.error(
            f"Exception {e.detail}\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(content={"msg": e.detail, "code": 2}, status_code=e.status_code)

    @app.exception_handler(RequestValidationError)
    async def all_exception_handler(request: Request, e: RequestValidationError):
        request.state.logger.error(
            f"Exception {e}\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(content={"msg": str(e), "code": 1}, status_code=417)
