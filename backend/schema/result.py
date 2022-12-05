from schema.basemodel import basemodel
from datetime import datetime
from typing import Optional


class Result(basemodel):
    id: int
    experiment_id: int
    dataset_id: int
    model: str
    result_json: Optional[str]
    result_text: Optional[str]
    visualization_path: Optional[str]
    finish_time: Optional[datetime]
    create_time: Optional[datetime]


class Result_Create(basemodel):
    experiment_id: int
    dataset_id: int
    model: str


class Result_Info(Result):
    pass
