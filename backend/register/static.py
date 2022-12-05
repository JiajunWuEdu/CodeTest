from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def register_static(app: FastAPI):
    app.mount(f"/static", StaticFiles(directory="static"), name="static")
