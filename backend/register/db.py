from peewee import MySQLDatabase
from fastapi import FastAPI, Request
from config import config

db = MySQLDatabase(
    config.MYSQL_NAME,
    host=config.MYSQL_HOST,
    port=config.MYSQL_PORT,
    user=config.MYSQL_USERNAME,
    password=config.MYSQL_PASSWORD,
    charset='utf8mb4',
    autoconnect=True
)


# db should be registered in the middleware - but not used with peewee
def register_db(app: FastAPI):
    @app.middleware("http")
    async def add_db_state(request: Request, call_next):
        if not hasattr(request.state, "db"):
            request.state.db = db
        response = await call_next(request)
        return response
