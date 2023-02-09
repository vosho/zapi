from elasticsearch import Elasticsearch

from system.libs.baseservice import BaseService


class EsService(BaseService):
    es = None
    auto_load = False

    def init(self, cfg = None):
        self.es = Elasticsearch([
            self.ctx.cfg.es.url
        ])

    def get_last_id(self, key):
        self.ctx.services.redis.incr(key)
        x = self.ctx.services.redis.get(key)
        return int(x)

    def __getattr__(self, item):
        keys = [
            ''
        ]
        if item not in keys:
            call = getattr(self.es, item)
        else:
            call = object.__getattribute__(self, item)

        def wrapper(*args, **kw):
            return call(*args, **kw)

        return wrapper
