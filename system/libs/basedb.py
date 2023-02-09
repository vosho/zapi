import logging
import os
import time

import moment as moment
import peewee
import playhouse
from peewee import MySQLDatabase, OperationalError, __exception_wrapper__, InterfaceError, Proxy, Database
from playhouse.pool import PooledMySQLDatabase, PooledPostgresqlExtDatabase, PooledDatabase


class RetryOperationalError(PooledDatabase, Database):
    def execute_sql(self, sql, params=None, commit=True):
        cursor = None
        try:
            pass
        except Exception as e:
            logging.exception('Closing stale error')
        try:
            cursor = super().execute_sql(sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        except playhouse.pool.MaxConnectionsExceeded as e:
            logging.debug('Class [%s] in use cnn = %d, max cnn = %d' % (type(self).__name__, len(self._in_use), self._max_connections))
            try:
                pass
            except Exception as e:
                pass
            self.close_stale(5)
            self.close_idle()
            time.sleep(2)
            logging.exception('playhouse.pool.MaxConnectionsExceeded')
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        except peewee.InterfaceError as e:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        finally:
            pass
        if len(self._in_use) > self._max_connections * 0.7:
            self.close_stale(10)
            pass
        elif len(self._in_use) > self._max_connections * 0.5:
            pass
        else:
            pass

        return cursor


class RetrySQLConnectorMyDatabase(RetryOperationalError, PooledMySQLDatabase):
    _instance = {}
    _last_time = moment.now().seconds

    @staticmethod
    def _get_db_instance(cfg, env, force=False):
        one_hour = 60 * 60
        elapse = moment.now().seconds - RetrySQLConnectorMyDatabase._last_time
        if env not in RetrySQLConnectorMyDatabase._instance or force is True or elapse > one_hour * 0.5:
            RetrySQLConnectorMyDatabase._instance[env] = RetrySQLConnectorMyDatabase(
                database=cfg['db'],
                user=cfg['user'],
                password=cfg['password'],
                host=cfg['host'],
                autocommit=True,
                autorollback=True,
                max_connections=2000,
                stale_timeout=300,
                # timeout=60*4
            )
        return RetrySQLConnectorMyDatabase._instance[env]


class RetrySQLConnectorPgDatabase(RetryOperationalError, PooledPostgresqlExtDatabase):
    _instance = {}
    _last_time = moment.now().seconds

    @staticmethod
    def _get_db_instance(cfg, env, force=False):
        one_hour = 60 * 60
        elapse = moment.now().seconds - RetrySQLConnectorPgDatabase._last_time
        if env not in RetrySQLConnectorPgDatabase._instance or force is True or elapse > one_hour * 0.5:
            RetrySQLConnectorPgDatabase._instance[env] = RetrySQLConnectorPgDatabase(
                database=cfg['db'],
                user=cfg['user'],
                password=cfg['password'],
                host=cfg['host'],
                port=cfg['port'] if 'port' in cfg else 5432,
                autocommit=True,
                autorollback=True,
                max_connections=500,
                stale_timeout=15,
                # timeout=60 * 4
            )
        return RetrySQLConnectorPgDatabase._instance[env]
