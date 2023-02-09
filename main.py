import argparse
import logging
import importlib

from system.libs.kit import Kit
from system.libs.logger import Logging


class Main:

    def __init__(self):
        parser = argparse.ArgumentParser(description='Input cmd:')
        parser.add_argument('-c', '--cmd', help='command to execute:test/task')
        parser.add_argument('-n', '--name', help='task or test name')
        args, unkonws = parser.parse_known_args()
        if not args.cmd:
            Logging('main_cmd')
            logging.exception('No cmd is specified')
        elif not args.name:
            Logging('main_cmd')
            logging.exception('No cmd name is specified')
        elif args.cmd == 'task':
            Logging('task_%s' % args.name)
            self.run_cmd(args.cmd, args.name, unkonws)
        elif args.cmd == 'test':
            Logging('test_%s' % args.name)
            self.run_cmd(args.cmd, args.name, unkonws)
        else:
            logging.exception('No cmd is specified')

    def run_cmd(self, cmd, name, params):
        logging.debug('starting task %s' % name)
        try:
            module_path = '%ss.%s%s' % (cmd, name.replace('_', '').replace('-', ''), cmd)
            imp = importlib.import_module(module_path)
            class_name = '%s%s' % (Kit.capitalize(name), Kit.capitalize(cmd))
            clazz = getattr(imp, class_name)
            instance = clazz()
            instance.set_params(params)
            instance.init()
            instance.run()
        except Exception as e:
            logging.exception(e)

    def run_test(self, name):
        pass


if __name__ == '__main__':
    Main()
