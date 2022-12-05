import peewee
from peewee import ForeignKeyField

from dbmodel.basemodel import basemodel, NoTZTimestampField
from dbmodel.project import Project


class Dataset(basemodel):
    project: ForeignKeyField = peewee.ForeignKeyField(column_name='project_id', field='id', model=Project, backref='datasets')
    name = peewee.CharField(max_length=255)
    file_path = peewee.CharField(max_length=255, default=None, null=True)
    row_count = peewee.IntegerField(default=None, null=True)
    visualization_path = peewee.CharField(max_length=255, default=None, null=True)
    upload_time = NoTZTimestampField(null=True, default=None)

    class Meta:
        table_name = "dataset"
