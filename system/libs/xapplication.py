# -- encoding=utf-8 --
import importlib
import logging
import multiprocessing
import os
import signal

import tornado
from tornado import web
from tornado.web import Application

from system.libs.configuration import Configuration
from system.libs.kit import Kit


class DefaultFileFallbackHandler(tornado.web.StaticFileHandler):

    def validate_absolute_path(self, root, absolute_path):
        try:
            absolute_path = super().validate_absolute_path(root, absolute_path)
        except tornado.web.HTTPError:
            root = os.path.abspath(root)
            absolute_path = os.path.join(root, self.default_filename)
        return absolute_path


class XApplication(Application):
    cfg = None
    services = {}
    interceptors = []

    def __init__(self, cfg_path='config.json'):
        self.cfg = Configuration(cfg_path)
        prefix = self.cfg.prefix if self.cfg.prefix else 'api/v1/'
        prefix = f'{prefix}{"" if prefix[-1] == "/" else "/"}'

        working_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        controller_dir = '/%s/controllers' % working_dir
        routes = []
        route_names = []
        static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'views/')
        if os.path.exists(controller_dir):
            for controller_name in os.listdir(controller_dir):
                if 'controller' in controller_name:
                    controller_name = controller_name.replace('controller', '')
                    controller_name = controller_name.replace('.py', '')
                    imp = importlib.import_module('controllers.%scontroller' % controller_name)
                    class_name = '%s%s' % (controller_name.capitalize(), 'Controller')

                    clazz = getattr(imp, class_name)
                    pattern = rf'/{prefix}{controller_name}/?.*'
                    logging.debug(f'Loading controller [{pattern} to {class_name}]')
                    routes.append((pattern, clazz, dict(ctx=self)))
                    route_names.append(controller_name)

        logging.debug('Init App with api routes %s', route_names)
        logging.debug('Init App with static routes %s', static_folder)

        # session configuration
        routes.append(
            (
                r"/(.*)", DefaultFileFallbackHandler, {
                    'path': 'views/',
                    'default_filename': 'index.html'
                }
            ),
        )
        settings = {
            'debug': True,
            'autoreload': True,
            'session': {
                'driver': 'memory',
                'driver_settings': {'host': self},
                'force_persistence': True,
                'sid_name': 'TSSSID',
                'session_lifetime': 1800
            },
            # 'static_path':  static_folder
        }
        super().__init__(routes, **settings)

        # init services
        self.__init_services()

    def init_web_containers(self):
        pass

    def add_interceptor(self, callback):
        self.interceptors.append(callback)

    def load_service(self, name):
        logging.debug('Loading service [%s]' % name)
        service_dir = 'services.%sservice' % name
        imp = importlib.import_module(service_dir)
        class_name = '%s%s' % (name.capitalize(), 'Service')
        clazz = getattr(imp, class_name)
        clazz_instance = clazz()
        clazz_instance.ctx = self
        clazz_instance.application = self
        clazz_instance.ctx = self
        clazz_instance.init()
        self.services.__dict__[name] = clazz_instance

    def start_task(self, name, args=()):
        # --------
        try:
            pfd = open('run/%s_run.pid' % name, 'r')
            if pfd is not None:
                pid = pfd.read(100)
                pid = int(pid)
                os.kill(pid, signal.SIGTERM)
                pfd.close()
        except Exception as e:
            logging.exception('killing task exception %s' % str(e))
            pass
        # --------
        p = multiprocessing.Process(target=XApplication.start_task_process, args=(name, args))
        p.start()
        pfd = open('run/%s_run.pid' % name, 'w')
        pfd.write('%d' % p.pid)
        pfd.close()

    def stop_task(self, name):
        # --------
        try:
            pfd = open('run/%s_run.pid' % name, 'r')
            if pfd is not None:
                pid = pfd.read(100)
                pid = int(pid)
                os.kill(pid, signal.SIGTERM)
                pfd.close()
        except Exception as e:
            # logging.exception('stop task exception %s' % str(e))
            pass
        # --------

    @staticmethod
    def start_task_process(name, args=()):
        logging.debug('Starting task [%s]' % name)
        try:
            # Logging(f'TaskProcess_{name}')
            import multiprocessing
            logger = multiprocessing.get_logger()
            logger.debug('Starting task process [%s]' % name)

            cmd = 'task'
            module_path = '%ss.%s%s' % (cmd, name.replace('_', '').replace('-', ''), cmd)
            imp = importlib.import_module(module_path)
            class_name = '%s%s' % (Kit.capitalize(name), Kit.capitalize(cmd))
            clazz = getattr(imp, class_name)
            instance = clazz()
            instance.init()
            instance.set_params(args)
            instance.run()
        except Exception as e:
            logging.exception(e)
            return -1

    def __init_services(self):
        self.services = self.Obj()
        working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        service_dir = '%s/services' % working_dir
        if os.path.exists(service_dir):
            for d in os.listdir(service_dir):
                if 'service' not in d:
                    # File Name
                    continue
                service_file_path = '%s/%s' % (service_dir, d)
                service_name = d.replace('service.py', '')
                imp = importlib.import_module('services.%sservice' % service_name)
                #

                #
                class_name = '%s%s' % (service_name.capitalize(), 'Service')
                clazz = getattr(imp, class_name)
                clazz_instance = clazz()
                if clazz_instance.auto_load:
                    logging.debug('Initializing service[%s]' % service_name)
                    clazz_instance.ctx = self
                    clazz_instance.application = self
                    clazz_instance.ctx = self
                    clazz_instance.init()
                    self.services.__dict__[service_name] = clazz_instance

    class Obj:
        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]
            else:
                raise Exception('Service %s not found' % item)
