from schema.basemodel import basemodel
from schema.project import Project_Name
from schema.dataset import Dataset_Info
from schema.result import Result_Info
from datetime import datetime
from typing import Optional


class Experiment(basemodel):
    id: int
    project_id: int
    dataset_id: Optional[int]
    name: str
    model: Optional[str]
    result_id: Optional[int]
    update_time: Optional[datetime]


class Experiment_Info(basemodel):
    id: int
    project: Optional[Project_Name]
    dataset: Optional[Dataset_Info]
    name: str
    model: Optional[str]
    result: Optional[Result_Info]
    update_time: Optional[datetime]


class Experiment_Name(basemodel):
    id: int
    name: str


class Experiment_Create(basemodel):
    project_id: int
    name: str


class Experiment_Save(basemodel):
    id: int
    dataset_id: Optional[int]
    model: Optional[str]
    result_id: Optional[int]