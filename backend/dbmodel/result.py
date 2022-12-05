import peewee
from dbmodel.basemodel import basemodel, NoTZTimestampField


class Result(basemodel):
    # Treat foreign keys as normal integers here to save system resource
    experiment_id = peewee.IntegerField(default=None)
    dataset_id = peewee.IntegerField(default=None)

    model = peewee.CharField(max_length=100, default=None)

    result_json = peewee.TextField(default=None, null=True)
    result_text = peewee.TextField(default=None, null=True)

    visualization_path = peewee.CharField(max_length=255, default=None, null=True)
    finish_time = NoTZTimestampField(default=None, null=True)

    class Meta:
        table_name = "result"
