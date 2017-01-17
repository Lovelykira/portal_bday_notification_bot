from peewee import Model, CharField, TimeField, ForeignKeyField
from playhouse.sqlite_ext import SqliteExtDatabase

import conf

db = SqliteExtDatabase(conf.DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class Subscriber(BaseModel):
    channel = CharField()


class SubscriberNotification(BaseModel):
    subscriber = ForeignKeyField(Subscriber)
    notification_name = CharField()
