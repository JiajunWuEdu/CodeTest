from fastapi import APIRouter, HTTPException
from playhouse.shortcuts import model_to_dict
from schema.experiment import Experiment_Name, Experiment_Create, Experiment_Info, Experiment_Save
from schema.general import ResponseModel
from dbmodel import Db_Experiment
from peewee import fn

router = APIRouter()


@router.get("/name", response_model=Experiment_Name, summary='get experiment name by id')
async def get_name(id: int):
    query = Db_Experiment.select(Db_Experiment.id, Db_Experiment.name).where(
        (Db_Experiment.id == id) & Db_Experiment.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Experiment not found")
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/create", response_model=Experiment_Info, summary='create a new experiment')
async def create(experiment: Experiment_Create = None):
    try:
        experiment_id = Db_Experiment.create(project_id=experiment.project_id, name=experiment.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Experiment not created")
    record = Db_Experiment.get(Db_Experiment.id == experiment_id)
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/rename", response_model=Experiment_Name, summary='update the experiment name')
async def rename(experiment: Experiment_Name = None):
    update_result = Db_Experiment \
        .update({"name": experiment.name}) \
        .where(Db_Experiment.id == experiment.id) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Name not updated")
    return await get_name(experiment.id)


@router.get("/delete", response_model=ResponseModel, summary='delete a experiment')
async def delete(id: int = None):
    update_result = Db_Experiment \
        .update({"delete_time": fn.now()}) \
        .where((Db_Experiment.id == id) & Db_Experiment.delete_time.is_null()) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Experiment deletion failed")
    return {'code': 0, 'msg': 'Done'}


@router.get("/info", response_model=Experiment_Info, summary='get experiment by id')
async def get_info(id: int = None):
    query = Db_Experiment.select().where(
        (Db_Experiment.id == id) & Db_Experiment.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Experiment not found")
    record_dict = model_to_dict(record, extra_attrs=['dataset_id', 'result_id'])
    return record_dict


@router.post("/save", response_model=Experiment_Info, summary='update the experiment record')
async def rename(experiment: Experiment_Save = None):
    update_result = Db_Experiment \
        .update({"dataset_id": experiment.dataset_id,
                 "model": experiment.model,
                 "result_id": experiment.result_id,
                 "update_time": fn.now()}) \
        .where(Db_Experiment.id == experiment.id) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Experiment record not updated")
    return await get_info(experiment.id)
