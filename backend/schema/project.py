from schema.basemodel import basemodel


class Project(basemodel):
    id: int
    name: str


class Project_Info(Project):
    dataset_count: int
    experiment_count: int


class Project_Name(basemodel):
    id: int
    name: str


class Project_Create(basemodel):
    name: str
