from peewee import Model, CharField
from playhouse.sqlite_ext import SqliteExtDatabase

import conf

db = SqliteExtDatabase(conf.DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class Subscriber(BaseModel):
    channel = CharField()
