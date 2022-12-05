import uvicorn
from fastapi import FastAPI
from register import register_static, register_db, register_exception, register_cors, register_logger, register_router
from config import config

from config import config
app = FastAPI()
app = FastAPI(description="myAPP", version="0.1")


@app.on_event("startup")
async def startup():
    register_db(app)
    register_router(app)
    register_static(app)
    register_exception(app)
    register_logger(app)
    register_cors(app)


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=config.BASE_PORT)
