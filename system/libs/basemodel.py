import json

import peewee
from peewee import Model
from playhouse.shortcuts import model_to_dict

from system.libs.kit import Kit



class ZeroCount:
    # @staticmethod
    def count(self):
        return 0


class BaseModel(Model):
    @classmethod
    def get_one_or_none(cls, *query, **kwargs):
        finds = cls.select().where(*query)
        if finds.count():
            return finds[0]
        return None

    @classmethod
    def get_all(cls, *query, **kwargs):
        if query:
            finds = cls.select().where(*query)
        else:
            finds = cls.select()
        if 'order' in kwargs:
            finds = finds.order_by(kwargs['order'])
        try:
            if finds.count():
                return finds
            else:
                return ZeroCount()
        except Exception as e:
            print(e)
            return ZeroCount()

    @classmethod
    def get_count(cls, *query, **kwargs):
        if query:
            finds = (cls.select(peewee.fn.COUNT(cls.id).alias('c')).where(*query))
        else:
            finds = (cls.select(peewee.fn.COUNT(cls.id).alias('c')))

        return finds.scalar()

    def to_json(self):
        return model_to_dict(self)

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    @classmethod
    def delete_with(cls,  *query, **kwargs):
        q = cls.delete().where(*query)
        q.execute()

    @classmethod
    def save_from_data(cls, data, only=[], where=None):
        find = None
        # if id in data:
        #     find = cls.get_or_none(cls[id] == data[id])
        if where:
            find = cls.get_or_none(where)
        if find:
            # update
            for k in find.__data__:
                if k in data:
                    setattr(find, k, data[k])
                if k == 'utime' and ('utime' not in data or not data['utime']):
                    now = Kit.datetime_now(['-', ' ', ':'])
                    data['utime'] = now
                    setattr(find, k, now)
            if len(only):
                find.save(only=only)
            else:
                #keys = data.keys()
                find.save()
            return find

        param = {}
        for k in cls.__dict__:
            if k[0] != '_' and k in data:
                param[k] = data[k]
            if k == 'ctime' and ('ctime' not in data or not data['ctime']):
                now = Kit.datetime_now(['-', ' ', ':'])
                param[k] = now
            if k == 'utime' and ('utime' not in data or not data['utime']):
                now = Kit.datetime_now(['-', ' ', ':'])
                param[k] = now
        return cls.create(**param)

    def set_meta(self):
        pass