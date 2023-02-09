import json
import logging
import os


class Configuration:
    cfg = {}

    def __init__(self, path='config.json'):
        self.load_config(path)

    def load_config(self, path):
        config_path = '%s/../%s' % (os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path)
        logging.debug('Loading config file %s' % config_path)
        if os.path.exists(config_path):
            fd = open(config_path, 'r')
            js = json.load(fd, object_hook=self.Obj)
            fd.close()
            self.cfg = js
        else:
            logging.error('config file not exists')
            raise Exception('Not Configuration File Found')

    def __getattr__(self, item):
        val = getattr(self.cfg, item)
        if val:
            return val
        else:
            raise Exception('Key %s is not found in cfg' % item)

    class Obj:
        def __init__(self, dct):
            self.__dict__.update(dct)

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]