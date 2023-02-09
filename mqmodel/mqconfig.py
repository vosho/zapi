from peewee import IntegerField, CharField

from system.libs.basemodel import BaseModel


class MqConfig(BaseModel):
    id = IntegerField(primary_key=True)
    key = CharField(max_length=255)
    val = CharField(max_length=255)
    description = CharField(max_length=255)

    class Meta:
        db_table = 'config'
