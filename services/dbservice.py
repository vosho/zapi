import importlib

from system.libs.basedb import RetrySQLConnectorMyDatabase, RetrySQLConnectorPgDatabase
from system.libs.baseservice import BaseService
from system.libs.modelfactory import construct_model


class DbService(BaseService):
    auto_load = True
    def __init__(self):
        self.envs = {}

    def init(self, cfg=None):
        db_source = self.ctx.cfg.dbsource.__dict__
        for k in db_source:
            cfg = db_source[k]
            RetrySQLConnectorClazz = RetrySQLConnectorMyDatabase if cfg.type == 'mysql' else RetrySQLConnectorPgDatabase
            self.envs[k] = RetrySQLConnectorClazz(
                database=cfg.db,
                user=cfg.user,
                password=cfg.password,
                host=cfg.host,
                port=cfg.port if cfg.port else 5432,
                autocommit=True,
                autorollback=True,
                max_connections=cfg.max_connections if cfg.max_connections else 200,
                stale_timeout=cfg.stale_timeout if cfg.stale_timeout else 100,
            )

    def get_connection(self, env):
        return self.envs[env]

    def load_model(self, model, env=None, table_name=None, folder='mqmodel'):
        if not env:
            env = self.ctx.cfg.env
        if env in self.envs:
            instance = self.envs[env]
            if type(instance) == RetrySQLConnectorMyDatabase:
                model_path = f'mqmodel.mq{model.lower()}'
                model_class = f'Mq{model}'
            else:
                model_path = f'{folder}.pg{model.lower()}'
                model_class = f'Pg{model}'

            try:
                ModelClazz = importlib.import_module(model_path)
                ModelInstance = getattr(ModelClazz, model_class)

                z = construct_model(model_class, ModelInstance, instance, table_name)
                return z
            except ModuleNotFoundError as e:
                return None
