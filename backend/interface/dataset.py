from fastapi import APIRouter, HTTPException, File, Form
from playhouse.shortcuts import model_to_dict
from schema.dataset import Dataset, Dataset_Name, Dataset_Create, Dataset_Info
from schema.general import ResponseModel
from dbmodel import Db_Dataset
from peewee import fn
import csv
import matplotlib.pyplot as plt

router = APIRouter()


@router.get("/name", response_model=Dataset_Name, summary='get dataset name by id')
async def get_name(id: int):
    query = Db_Dataset.select(Db_Dataset.id, Db_Dataset.name).where(
        (Db_Dataset.id == id) & Db_Dataset.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Dataset not found")
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/create", response_model=Dataset_Info, summary='create a new dataset')
async def create(dataset: Dataset_Create = None):
    try:
        dataset_id = Db_Dataset.create(project_id=dataset.project_id, name=dataset.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Dataset not created")
    record = Db_Dataset.get(Db_Dataset.id == dataset_id)
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/rename", response_model=Dataset_Name, summary='update the dataset name')
async def rename(dataset: Dataset_Name = None):
    update_result = Db_Dataset \
        .update({"name": dataset.name}) \
        .where((Db_Dataset.id == dataset.id) & Db_Dataset.delete_time.is_null()) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Name not updated")
    return await get_name(dataset.id)


@router.get("/delete", response_model=ResponseModel, summary='delete a dataset')
async def delete(id: int = None):
    update_result = Db_Dataset \
        .update({"delete_time": fn.now()}) \
        .where((Db_Dataset.id == id) & Db_Dataset.delete_time.is_null()) \
        .execute()
    if not update_result:
        raise HTTPException(status_code=500, detail="Dataset deletion failed")
    return {'code': 0, 'msg': 'Done'}


@router.get("/info", response_model=Dataset_Info, summary='get dataset name by id')
async def get_info(id: int = None):
    query = Db_Dataset.select().where(
        (Db_Dataset.id == id) & Db_Dataset.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Dataset not found")
    record_dict = model_to_dict(record)
    return record_dict


@router.post("/upload", response_model=Dataset_Info, summary='upload a new dataset file')
async def create(file: bytes = File(), id: str = Form()):
    query = Db_Dataset.select().where(
        (Db_Dataset.id == id) & Db_Dataset.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    if record.upload_time:
        raise HTTPException(status_code=500, detail="Dataset file exists.")
    try:
        file_path = 'static/dataset/' + str(record.id) + '.csv'
        f = open(file_path, 'wb')
        f.write(file)
        f.close()
        input_file = open(file_path, "rU")
        reader_file = csv.DictReader(input_file)
        row_count = len(list(reader_file))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not save and parse the file.")
    if row_count <= 0:
        raise HTTPException(status_code=500, detail="The file is empty.")
    record.row_count = row_count
    record.file_path = file_path
    record.upload_time = fn.now()
    record.save()
    record_dict = await get_info(id)
    return record_dict


@router.get("/visualize", response_model=Dataset_Info, summary='get visualization by id')
async def visualize(id: int = None):
    query = Db_Dataset.select().where(
        (Db_Dataset.id == id) & Db_Dataset.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if not record.visualization_path:
        try:
            file_path = 'static/dataset/' + str(record.id) + '.csv'
            visualization_path = 'static/dataset/' + str(record.id) + '.png'
            input_file = open(file_path, "rU")
            reader_file = csv.DictReader(input_file)
            x = []
            y = []
            for row in reader_file:
                x.append(float(row['x']))
                y.append(float(row['y']))
            fig = plt.figure(figsize=(6, 6), dpi=300)
            ax = fig.add_subplot(1, 1, 1)
            ax.scatter(x, y)
            fig.savefig(visualization_path)
            record.visualization_path = visualization_path
            record.save()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Could not visualize the file.")

    record_dict = model_to_dict(record)
    return record_dict