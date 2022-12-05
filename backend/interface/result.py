from fastapi import APIRouter, Depends, HTTPException, status
from playhouse.shortcuts import model_to_dict
from schema.result import Result, Result_Create, Result_Info
from dbmodel import Db_Dataset, Db_Result
import json, csv, time
from peewee import fn
import _thread as thread
from scipy.stats import linregress
import matplotlib.pyplot as plt

router = APIRouter()


@router.post("/create", response_model=Result_Info, summary='create a new computation')
async def create(result: Result_Create = None):
    try:
        result_id = Db_Result.create(experiment_id=result.experiment_id, dataset_id=result.dataset_id,
                                     model=result.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Result not created.")
    record = Db_Result.get(Db_Result.id == result_id)
    record_dict = model_to_dict(record)
    try:
        thread.start_new_thread(compute, (record_dict,))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Result computation thread failed to start.")
    return record_dict


def compute(result: Result_Info = None):
    if not result:
        raise HTTPException(status_code=500, detail="Cannot start the computation.")
    query = Db_Dataset.select().where((Db_Dataset.id == result['dataset_id']) & Db_Dataset.delete_time.is_null())
    record = query.get_or_none()
    dataset = model_to_dict(record)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if dataset['row_count'] is not None and dataset['row_count'] > 0:
        file_path = 'static/dataset/' + str(record.id) + '.csv'
        input_file = open(file_path, "rU")
        reader_file = csv.DictReader(input_file)
        if result['model'] == 'linear':
            x = []
            y = []
            for row in reader_file:
                x.append(float(row['x']))
                y.append(float(row['y']))
            print('Computation Start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            model_result = linregress(x, y)
            result_json_dict = {"slope": model_result.slope, "intercept": model_result.intercept,
                                "rvalue": model_result.rvalue, "pvalue": model_result.pvalue}
            result_text = "y = {:.2f} * x + {:.2f} (R2 = {:.2f})".format(
                model_result.slope, model_result.intercept, model_result.rvalue ** 2)

            print('Sleep 5!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            time.sleep(5)

            print('Computation OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        else:
            raise HTTPException(status_code=500, detail="Unknown data analysis model.")
        result_json = json.dumps(result_json_dict)
        update_result = Db_Result \
            .update({"result_json": result_json, "result_text": result_text, "finish_time": fn.now()}) \
            .where(Db_Result.id == result['id']) \
            .execute()
        if not update_result:
            raise HTTPException(status_code=500, detail="Result not saved")
    else:
        raise HTTPException(status_code=500, detail="Dataset is not ready for use.")


@router.get("/info", response_model=Result_Info, summary='get the result by id')
async def get_info(id: int = None):
    query = Db_Result.select().where(
        (Db_Result.id == id) & Db_Result.delete_time.is_null())
    record = query.get_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Result not found.")
    record_dict = model_to_dict(record)
    return record_dict


@router.get("/visualize", response_model=Result_Info, summary='get visualization by id')
async def visualize(id: int = None):
    query = Db_Result.select().where(
        (Db_Result.id == id) & Db_Result.delete_time.is_null())
    result = query.get_or_none()
    if not result or not result.finish_time:
        raise HTTPException(status_code=404, detail="Result not ready")

    if not result.visualization_path:
        query = Db_Dataset.select().where(
            (Db_Dataset.id == result.dataset_id) & Db_Dataset.delete_time.is_null())
        dataset = query.get_or_none()
        if not dataset or not dataset.file_path:
            raise HTTPException(status_code=404, detail="Dataset not found")
        try:
            visualization_path = 'static/result/' + str(result.id) + '.png'
            result_json_dict = json.loads(result.result_json)
            input_file = open(dataset.file_path, "rU")
            reader_file = csv.DictReader(input_file)
            x = []
            y = []
            for row in reader_file:
                x.append(float(row['x']))
                y.append(float(row['y']))
            fig = plt.figure(figsize=(6, 6), dpi=300)
            ax = fig.add_subplot(1, 1, 1)
            ax.scatter(x, y)
            ax.axline((0, result_json_dict['intercept']), slope=result_json_dict['slope'], color='r')
            fig.savefig(visualization_path)
            result.visualization_path = visualization_path
            result.save()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Could not visualize the result.")

    record_dict = model_to_dict(result)
    return record_dict
