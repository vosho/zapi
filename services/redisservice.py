import logging

import redis as redis

from system.libs.baseservice import BaseService


class RedisService(BaseService):
    redis = None
    auto_load = False

    def init(self, cfg=None):
        logging.debug('RedisService Initiating')
        redisconfig = cfg if cfg else self.application.cfg.redis
        self.redis = redis.StrictRedis(
            host=redisconfig.host,
            port=redisconfig.port,
            password=redisconfig.password,
            db=redisconfig.db,
            decode_responses=True,
        )

    def delete(self, key):
        for k in self.keys(key):
            self.redis.delete(k)

    def __getattr__(self, item):
        keys = [
            'incr', 'setnx', 'keys', 'smembers', 'sadd', 'get', 'set', 'setex', 'scard', 'sismember', 'srem'
        ]
        if item in keys:
            call = getattr(self.redis, item)
        else:
            call = object.__getattribute__(self, item)

        def wrapper(*args, **kw):
            return call(*args, **kw)

        return wrapper
