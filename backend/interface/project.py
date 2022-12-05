from fastapi import APIRouter, HTTPException
from playhouse.shortcuts import model_to_dict
from typing import List
from schema.project import Project, Project_Info, Project_Name, Project_Create
from schema.dataset import Dataset_Info
from schema.experiment import Experiment_Info
from schema.general import ResponseModel
from dbmodel import Db_Project, Db_Dataset, Db_Experiment
from peewee import fn, JOIN

router = APIRouter()


@router.get("/list", response_model=List[Project_Info], summary='get list of projects')
async def get_list():
    project_list = list()
    query = Db_Project.select(
        Db_Project,
        Db_Dataset.select(fn.count(1)).where((Db_Dataset.project_id==Db_Project.id) & Db_Dataset.delete_time.is_null()).alias('dataset_count'),
        Db_Experiment.select(fn.count(1)).where((Db_Experiment.project_id==Db_Project.id) & Db_Experiment.delete_time.is_null()).alias('experiment_count')
    ).where(Db_Project.delete_time.is_null()).order_by(-Db_Project.id)
    for record in query:
        record_dict = model_to_dict(record, fields_from_query=query, extra_attrs=['dataset_count','experiment_count'])
        project_list.append(record_dict)
    return project_list


@router.get("/datasets", response_model=List[Dataset_Info], summary='get list of datasets by project id')
async def get_datasets(id: int):
    dataset_list = list()
    query = Db_Dataset.select().where((Db_Dataset.project_id == id) & Db_Dataset.delete_time.is_null()).order_by(
        -Db_Dataset.id)
    for record in query:
        record_dict = model_to_dict(record, fields_from_query=query, recurse=False)
        dataset_list.append(record_dict)
    return dataset_list


@router.get("/experiments", response_model=List[Experiment_Info], summary='get list of experiments by project id')
async def get_datasets(id: int):
    experiment_list = list()
    query = Db_Experiment.select().where(
        (Db_Experiment.project_id == id) & Db_Experiment.delete_time.is_null()).order_by(-Db_Experiment.id)
    for record in query:
        record_dict = model_to_dict(record, recurse=True)
        experiment_list.append(record_dict)
    return experiment_list


@router.get("/name", response_model=Project_Name, summary='get name by id')
async def get_name(id: int):
    query = Db_Project.select(Db_Project.id, Db_Project.name).where(
        (Db_Project.id == id) & Db_Project.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Project not found")
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/create", response_model=Project, summary='create a new project')
async def create(project: Project_Create = None):
    try:
        project_id = Db_Project.create(name=project.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Project not created")
    record = Db_Project.get(Db_Project.id == project_id)
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/rename", response_model=Project_Name, summary='update the project name')
async def edit_theme(project: Project_Name = None):
    update_result = Db_Project \
        .update({"name": project.name}) \
        .where((Db_Project.id == project.id) & Db_Project.delete_time.is_null()) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Name not updated")
    return await get_name(project.id)


@router.get("/delete", response_model=ResponseModel, summary='delete a project')
async def delete(id: int = None):
    update_result = Db_Project \
        .update({"delete_time": fn.now()}) \
        .where((Db_Project.id == id) & Db_Project.delete_time.is_null()) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Project deletion failed")
    return {'code': 0, 'msg': 'Done'}
