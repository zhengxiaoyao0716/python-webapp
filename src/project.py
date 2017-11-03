# -*- coding: utf-8 -*-

"""
Project define.
"""


def immediate(*args, **kwargs):
    """execute function immediately"""
    def decorate(fn):
        fn(*args, **kwargs)
    return decorate


@immediate('project.json')
def _read_config(path):
    global NAME
    global VERSION
    global MODULES
    from json import load
    with open(path) as f:
        config = load(f)
        NAME = config['name']
        VERSION = config['version']
        MODULES = config['modules']


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
    DB = namedtuple('_DB', ('engine', 'session'))(engine, session)
