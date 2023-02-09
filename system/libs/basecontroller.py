import json
import logging
from json import JSONDecodeError

import tornado
from playhouse.shortcuts import model_to_dict
from torndsession.sessionhandler import SessionBaseHandler

from system.libs.baseobj import BaseObj
from system.libs.finishexception import FinishException


class BaseController(SessionBaseHandler):
    application = None
    ctx = None
    finished = False

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def initialize(self, ctx):
        self.ctx = ctx

    def prepare(self):
        super().prepare()
        logging.debug('BaseController prepare')

        self.ctx = self.application
        for i in self.application.interceptors:
            typename = str(type(i))
            if 'class' in typename:
                if not i.do(self.application, self.request):
                    self.write('End')
                    self.finish('End')
            else:
                if not i(self.application, self.request):
                    self.write('End')
                    self.finish('End')

    def __dispatch(self):
        uri = self.request.uri
        if not uri:
            self.make_alert('Parameter Error')
        segs = uri.split('?')
        if len(segs):
            uri = segs[0]
        segs = uri.split('/')
        if len(segs) < 4:
            return self.make_alert('Parameter Error')
        elif len(segs) == 4:
            method_name = 'index'
        else:
            method_name = '_'.join(segs[4:]).replace('/', '')

        method_type = self.request.method.lower()
        full_method_name = '%s_%s' % (method_type, method_name)
        logging.debug('calling method %s' % full_method_name)

        if full_method_name in self.__dict__:
            return self.make_alert('Method[%s] not implemented' % method_name)
        has_method = hasattr(self, full_method_name)
        if has_method:
            method = getattr(self, full_method_name)
            try:
                method()
            except FinishException as e:
                self.make_500(str(e))
                pass
        else:
            return self.make_alert('Method[%s] Not Found' % method_name)

    def get(self):
        try:
            self.__dispatch()
        except FinishException:
            pass

    def post(self):
        try:
            self.__dispatch()
        except FinishException:
            pass

    def __write(self, data):
        if not self.finished:
            self.write(data)

    def __finish(self):
        self.finished = True

    def end(self):
        self.__finish()
        #raise FinishException('Finished')

    def get_pager(self):
        page_size = int(self.get_argument('pagesize', '15'))
        page_index = int(self.get_argument('page', '0'))
        pager = {
            'pagesize': page_size,
            'page': page_index,
        }
        pager_string = json.dumps(pager)
        return json.loads(pager_string, object_hook=BaseObj)

    def purify_data(self, data):
        if type(data).__name__ == 'ModelSelect':
            if data.count():
                if 'Model' in str(type(data[0])):
                    data = [model_to_dict(d, recurse=True) for d in data]
                    # data = [self.model_to_dict(d) for d in data]
            else:
                data = []
        else:
            if 'Model' in str(type(data)):
                data = model_to_dict(data)
        return data

    def make_pager_result(self, data, pager=None):
        data = self.purify_data(data)
        result = {
            'data': data,
            'pager': pager.__dict__ if pager else {}
        }
        ret = {
            'type': type(data).__name__,
            'result': result,
            'state': 0,
            'msg': '',
        }

        self.__write(json.dumps(ret))

    def make_result(self, data):
        data = self.purify_data(data)
        result = {'data': data}
        ret = {
            'type': type(data).__name__,
            'result': result,
            'state': 0,
            'msg': ''
        }
        self.__write(json.dumps(ret))
        self.end()

    def make_alert(self, msg):
        result = {
            'msg': msg,
            'state': -1,
            'cmd': 'alert'
        }
        self.__write(json.dumps(result))
        self.end()

    def make_msg(self, msg, data={}):
        data = self.purify_data(data)
        result = {
            'msg': msg,
            'state': 0,
            'cmd': 'msg',
            'result': {
                'data': data
            }
        }
        self.__write(json.dumps(result))
        self.end()

    def make_login(self, msg):
        result = {
            'msg': msg,
            'state': -1,
            'cmd': 'login'
        }
        self.__write(json.dumps(result))
        self.end()

    def make_reg(self, msg = ''):
        result = {
            'msg': msg,
            'state': -1,
            'cmd': 'reg'
        }
        self.__write(json.dumps(result))
        self.end()

    def make_500(self, msg):
        self.__write(msg)

    def get_post_json(self):
        data = {}
        if self.request.method == 'POST':
            try:
                data = tornado.escape.json_decode(self.request.body)
            except JSONDecodeError as e:
                raise FinishException('Post Data is not json format')
        return data

    def get_param_data(self):
        data = {}
        for k in self.request.arguments:
            data[k] = self.get_argument(k)
        return data

    def get_client_ip(self):
        client_ip = self.request.headers.get("X-Real-IP") or \
                    self.request.headers.get("X-Forwarded-For") or \
                    self.request.remote_ip
        return client_ip
