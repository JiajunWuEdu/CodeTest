import peewee
from register.db import db
import datetime


class NoTZTimestampField(peewee.TimestampField):
    def db_value(self, value):
        if value is not None:
            return value.replace(tzinfo=None)
        else:
            return None


class basemodel(peewee.Model):
    id = peewee.AutoField(default=None)
    create_time = NoTZTimestampField(null=False)
    delete_time = NoTZTimestampField(null=True, default=None)

    class Meta:
        database = db
