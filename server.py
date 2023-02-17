# -- encoding=utf-8 --
import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from system.libs.xapplication import XApplication
from system.libs.logger import Logging


def main():
    Logging('server')
    app = XApplication()
    http_server = HTTPServer(app)
    http_server.listen(app.cfg.server.port or 17002)
    logging.debug('Starting http server http://127.0.0.1:%d' % app.cfg.server.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
