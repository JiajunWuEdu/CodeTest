from schema.basemodel import basemodel
from datetime import datetime
from typing import Optional


class Dataset(basemodel):
    id: int
    project_id: int;
    name: str
    file_path: Optional[str]
    row_count: Optional[int]
    visualization_path: Optional[str]
    upload_time: Optional[datetime]
    create_time: Optional[datetime]
    delete_time: Optional[datetime]


class Dataset_Info(basemodel):
    id: int
    project_id: Optional[int];
    name: str
    file_path: Optional[str]
    row_count: Optional[int]
    visualization_path: Optional[str]
    upload_time: Optional[datetime]


class Dataset_Create(basemodel):
    project_id: int
    name: str


class Dataset_Name(basemodel):
    id: int
    name: str
