import importlib
import inspect
import logging
from multiprocessing.context import BaseContext
from system.libs.xapplication import XApplication


class BaseTask(BaseContext):
    params = None

    def __init__(self):
        self.ctx = self.application = XApplication()

    def __init_logging(self):
        logging.basicConfig(
            filename='aitask.log',
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s  {%(filename)s:%(lineno)d} - %(message)s',
            datefmt='%H:%M:%S',
        )

        logging.getLogger('requests').setLevel(logging.ERROR)
        logging.getLogger('connectionpool').setLevel(logging.ERROR)
        logging.getLogger('peewee').setLevel(logging.ERROR)
        logging.getLogger('tornado.access').setLevel(logging.ERROR)
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        logging.getLogger('elasticsearch').setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

        stderrLogger = logging.StreamHandler()
        stderrLogger.setFormatter(
            logging.Formatter('[%(name)s] %(asctime)s] %(levelname)s  {%(filename)-16s:%(lineno)d} - %(message)s'))
        logging.getLogger().addHandler(stderrLogger)

    def init(self):
        pass

    def set_params(self, params):
        self.params = params

    def get_params(self):
        return self.params

    def get_param(self, index):
        if index >= len(self.params):
            return None
        else:
            return self.params[index]

    def run(self):
        for x in inspect.getmembers(self):
            method_name = x[0]
            if 'task_' in method_name:
                method = getattr(self, method_name)
                method()
