import peewee
from dbmodel.basemodel import basemodel, NoTZTimestampField
from dbmodel.project import Project
from dbmodel.dataset import Dataset
from dbmodel.result import Result


class Experiment(basemodel):
    project = peewee.ForeignKeyField(column_name='project_id', field='id', model=Project, backref='experiments')
    dataset = peewee.ForeignKeyField(column_name='dataset_id', field='id', model=Dataset)
    name = peewee.CharField(max_length=255)
    model = peewee.CharField(max_length=100, default=None, null=True)
    result = peewee.ForeignKeyField(column_name='result_id', field='id', model=Result)
    update_time = NoTZTimestampField(null=True, default=None)

    class Meta:
        table_name = "experiment"
