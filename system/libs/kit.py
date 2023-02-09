import math
import random
import re
import time
import uuid
from sys import exc_info
from traceback import format_exception

import moment
from datetime import datetime, date, timedelta


class Kit:
    @staticmethod
    def get_dir():
        pass

    @staticmethod
    def date_now(diff=0):
        return moment.now().add(days=diff).format('YYYY-MM-DD')
    @staticmethod
    def timestamp():
        return math.floor(datetime.now().timestamp() * 1000)

    @staticmethod
    def now(diff=0):
        return moment.now()

    @staticmethod
    def week_now(diff=0):
        week = moment.now().add(weeks=diff).date.isocalendar()[1]
        return '%s%02d' % (Kit.year_now(), week)

    @staticmethod
    def month_now(diff=0):
        if diff == 0:
            return moment.now().add(months=diff).format('YYYYMM')
        else:
            today = date.today()
            lastMonth = today - timedelta(months=1)
            print('-----' + lastMonth.strftime("%Y%m"))

    @staticmethod
    def day_now(diff=0, format='YYYYMMDD'):
        return moment.now().add(days=diff).format(format)

    @staticmethod
    def hour_now(diff=0, format='YYYYMMDDHH'):
        return moment.now().add(hours=diff).format(format)

    @staticmethod
    def minute_now(diff=0):
        return moment.now().add(hours=diff).format('YYYYMMDDHH')

    @staticmethod
    def year_now():
        now = datetime.now()
        return now.strftime('%Y')

    # @staticmethod
    # def datetime_now():
    #     now = datetime.now()
    #     return now.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def datetime_now(seps=None):
        if seps is None:
            seps = ['', '', '']
        now = datetime.now()
        sep0 = seps[0]
        sep1 = seps[1]
        sep2 = seps[2]
        return now.strftime('%Y' + sep0 + '%m' + sep0 + '%d' + sep1 + '%H' + sep2 + '%M' + sep2 + '%S')

    @staticmethod
    def capitalize(s):
        def c(x):
            x = x.group(0)
            x = x.replace('_', '')
            x = x.replace('-', '')
            x = x.upper()
            return x

        return re.sub(r'([_|\-][a-z]|^[a-z])', c, s)

    @staticmethod
    def get_month_start_end_datetime(offset=0):
        m = moment.now().add(months=offset)
        s = m.format('YYYY-MM-01 00:00:00')
        e = moment.now().add(months=offset + 1).format('YYYY-MM-01 00:00:00')
        return s, e, m

    @staticmethod
    def get_day_start_end_datetime(offset=0):
        d = moment.now().add(days=offset)
        s = d.format('YYYY-MM-DD 00:00:01')
        e = moment.now().add(days=offset + 1).format('YYYY-MM-DD 00:00:00')
        return s, e, d

    @staticmethod
    def get_hour_start_end_datetime(offset=0):
        d = moment.now().add(hours=offset)
        s = d.format('YYYY-MM-DD HH:00:01')
        e = moment.now().add(hours=offset + 1).format('YYYY-MM-DD HH:00:00')
        return s, e, d

    @staticmethod
    def get_moment(months=0, days=0, hours=0):
        m = moment.now()
        m.add(months=months).add(days=days).add(hours=hours)
        return m

    @staticmethod
    def calc_timestamp(m):
        x = datetime(m.year, m.month, m.day, m.hour, m.minute, m.second)
        return int(x.timestamp())

    @staticmethod
    def get_datetime_diff_with_object(datatime):
        return Kit.get_datetime_diff(datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        
    @staticmethod
    def get_datetime_diff_with_string(datatime_string):
        #2022-01-01 22:55:22
        year = datatime_string[0:4]
        month = datatime_string[5:7]
        day = datatime_string[8:10]
        hour = datatime_string[8:10]
        minute = datatime_string[11:13]
        second = datatime_string[14:16]
    @staticmethod
    def get_datetime_diff(year, month, day, hour, minute, second):
        diff = Kit.calc_timestamp(moment.now()) - Kit.calc_timestamp(moment.date(year, month, day, hour, minute, second))
        diff_total = diff = int(diff)
        #print(f'{Kit.calc_timestamp(moment.now())} - {Kit.calc_timestamp(moment.date(year, month, day, hour, minute, second))}')
        diff_readable = ''
        if diff > 3600:
            diff_readable += f'{int(diff / 3600)}小时'
            diff = diff % 3600
        if diff > 60:
            diff_readable += f'{int(diff / 60)}分'
            diff = diff % 60
        
        diff_readable += f'{diff % 60} Seconds'
        
        return diff_total , diff_readable

    @staticmethod
    def gene_uuid_plain():
        # rnd = random.Random()
        # rnd.seed(0)  # NOTE: Of course don't use a static seed in production
        # random_uuid = uuid.UUID(int=rnd.getrandbits(128), version=4)
        # return re.sub(r'\-', '', str(random_uuid)).upper()

        new_uuid = str(uuid.uuid4())
        return re.sub(r'\-', '', str(new_uuid)).upper()

    @staticmethod
    def rand_int(min, max):
        rnd = random.Random()
        rdm = rnd.random() * (max - min) * 11
        return math.ceil(rdm * 11) % (max - min + 1) + min


    @staticmethod
    def last_exception():
        etype, value, tb = exc_info()
        info, error = format_exception(etype, value, tb)[-2:]
        error = error[:-1]
        return error

    @staticmethod
    def get_milliseconds():
        return round(time.time() * 1000)
if __name__ == '__main__':
    print(Kit.month_now(-1))
    print(Kit.month_now(0))
    print(Kit.date_now(-1))
