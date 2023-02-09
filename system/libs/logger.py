import logging

from system.libs.kit import Kit


class Logger:
    def __init__(self, name, rotate=False):
        if rotate == 'date':
            suffix = Kit.date_now()
        elif rotate == 'datetime':
            suffix = Kit.datetime_now()
        else:
            suffix = 'r_'
        logging.basicConfig(
            filename='logs/%s_%s.log' % (name, suffix),
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s  {%(filename)s:%(lineno)d} - %(message)s',
            datefmt='%H:%M:%S',
        )

        logging.getLogger('requests').setLevel(logging.ERROR)
        logging.getLogger('connectionpool').setLevel(logging.ERROR)
        logging.getLogger('peewee').setLevel(logging.ERROR)
        # logging.getLogger('tornado.access').setLevel(logging.ERROR)
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        # logging.getLogger('root').setLevel(logging.ERROR)
        logging.getLogger('elasticsearch').setLevel(logging.ERROR)
        logging.getLogger('io_services_utils').setLevel(logging.ERROR)
        logging.getLogger('pika').setLevel(logging.ERROR)
        logging.getLogger('scrapy').setLevel(logging.ERROR)
        logging.getLogger('selenium').setLevel(logging.ERROR)
        logging.getLogger('scrapy.spiders').setLevel(logging.ERROR)
        logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

        logging.getLogger('scrapy').propagate = False
        logging.getLogger('matplotlib.font_manager').disabled = True

        stderrLogger = logging.StreamHandler()
        # [%(module)s]
        stderrLogger.setFormatter(
            logging.Formatter('[%(asctime)s] %(levelname)s  {%(filename)s:%(lineno)03d} - %(message)s'))
        logging.getLogger().addHandler(stderrLogger)
        self.logging = logging
        self.logger = logging.getLogger

    def get_logger(self):
        return logging.getLogger

    def get_logging(self):
        return self.logging