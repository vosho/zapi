import re


class BaseMeta:
    schema = 'v1'
    table_name = ''
    database = ''


def construct_model(model_name, clazz, instance, table_name = None):
    if table_name is None:
        table_name = model_name.replace('Pg', '').replace('Mq', '')
        table_name = re.sub('([a-z])([A-Z])', '\\1_\\2', table_name)
        table_name = table_name.lower()
    Meta = type('Meta', (BaseMeta,), {
        'database': instance,
        'table_name': clazz._meta.table_name or table_name
    })

    return type(model_name, (clazz,), {
        'Meta': Meta
    })
