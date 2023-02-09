import inspect
import sys

from system.libs.basecontext import BaseContext
from system.libs.xapplication import XApplication


class Color:
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"


class BaseTest(BaseContext):
    application = None
    params = []

    def __init__(self):
        self.init_logging()
        self.ctx = self.application = XApplication()

    def init_logging(self):
        pass

    def init(self):
        pass

    def before(self):
        pass

    def after(self):
        pass

    def set_params(self, params):
        self.params = params

    def run(self):
        stdprints = []
        line_length = 80
        print('*' * 80)
        class_name = self.__class__.__name__

        #DbHandler.refresh_proxy(self.ctx.cfg.postgres)
        self.before()

        print('Test Suite: ', end="")
        sys.stdout.write(Color.BLUE)
        print(class_name)
        for x in inspect.getmembers(self):
            method_name = x[0]
            if 'test_' in method_name:
                method = getattr(self, method_name)

                # ---------------------------------
                from io import StringIO
                stdout = sys.stdout
                sys.stdout = stringio = StringIO()
                rt = method()

                split_lines = stringio.getvalue().splitlines()
                if len(split_lines):
                    stdprints.append('~' * 40)
                    stdprints.append('%s.%s: ' % (class_name, method_name))
                    for line in split_lines:
                        stdprints.append(line)
                sys.stdout = stdout
                # ---------------------------------
                state = 'SUCCESS' if rt else 'FAILED'
                dot_line_length = line_length - len(state) - len(method_name) - len('case: ') - 2
                sys.stdout.write(Color.CYAN)
                print('case: %s %s ' % (method_name, '-' * dot_line_length), end='')
                if state == 'SUCCESS':
                    sys.stdout.write(Color.RESET)
                    sys.stdout.write(Color.GREEN)
                    print(state)
                else:
                    sys.stdout.write(Color.RED)
                    print(state)
                sys.stdout.write(Color.RESET)
        print('_' * 80)
        sys.stdout.write(Color.BOLD)
        print('LOG:')
        sys.stdout.write(Color.RESET)
        print('\n'.join(stdprints))
        print('-' * 80)

        self.after()
