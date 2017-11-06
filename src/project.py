# -*- coding: utf-8 -*-

"""
Project define.
"""


def immediate(*args, **kwargs):
    """execute function immediately"""
    def decorate(fn):
        fn(*args, **kwargs)
    return decorate


NAME = 'name'
VERSION = 'v1'
MODULES = ['guide', 'user', 'view']


@immediate()
def _environ_variables():
    global SECRET_KEY
    global DB_CONNECT
    from os import environ
    SECRET_KEY = environ.get('SECRET_KEY', 'SECRET_KEY')
    # mysql+pymysql://{{account}}:{{password}}@{{serverIp}}:{{port}}/{{dbName}}?charset={{charset}}
    DB_CONNECT = environ.get('DB_CONNECT', 'sqlite:///.%s.db' % NAME)


@immediate(DB_CONNECT)
def _init_database(db_connect):
    global DB
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    from collections import namedtuple
    engine = create_engine(
        db_connect, echo=False, encoding='utf8', convert_unicode=True,
    )
    session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    session.commit()
    DB = namedtuple('DB', ('engine', 'session'))(engine, session)


@immediate()
def _init_logger():
    global LOGGER

    class Logger(object):
        def __init__(self, logger):
            self.logger = logger

        def warning(self, *args, **kwargs):
            self.logger.warning(*args, **kwargs)

        def error(self, *args, **kwargs):
            self.logger.error(*args, **kwargs)

        def info(self, *args, **kwargs):
            self.logger.info(*args, **kwargs)

        def set_logger(self, logger):
            self.logger = logger
    LOGGER = Logger(type('Logger', (object,), {
        'warning': print,
        'error': print,
        'info': print,
    }))


CODE_USAGE = {
    '/guide/password/reset': {
        'text': '重置密码',
        'expiry': 3 * 60,
    },
    '/user/destroy': {
        'text': '销毁帐号',
        'expiry': 3 * 60,
    },
}
