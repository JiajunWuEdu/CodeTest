from fastapi import FastAPI, Security

from interface import project, dataset, experiment, result


def register_router(app: FastAPI):
    app.include_router(project.router, prefix='/project')
    app.include_router(dataset.router, prefix='/dataset')
    app.include_router(experiment.router, prefix='/experiment')
    app.include_router(result.router, prefix='/result')
