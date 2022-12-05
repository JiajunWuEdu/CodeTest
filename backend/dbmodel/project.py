import peewee
from dbmodel.basemodel import basemodel


class Project(basemodel):
    name = peewee.CharField(max_length=255)

    class Meta:
        table_name = "project"


