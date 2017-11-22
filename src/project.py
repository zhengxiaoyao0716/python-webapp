# -*- coding: utf-8 -*-

NAME = 'project'  # $项目名称
VERSION = 'v1'  # $版本号

if __name__ == '__main__':
    from os import environ, path, rename, remove
    from re import match
    from sys import exit
    producers = {
        'NAME': lambda v: v,
        'VERSION': lambda v: 'v%d' % (1 + int(v[1:])),
    }
    src = environ.get('SRC', '')
    raw_path = path.join(src, 'project.py')
    new_path = path.join(src, 'project.py.new')
    with open(raw_path, 'r', encoding='utf-8') as raw_file, \
            open(new_path, 'w', encoding='utf-8') as new_file:
        for line in raw_file.readlines():
            m = match('^(\w+) = \'(\w+)\'  # \$(\w+)$', line)
            if not m:
                new_file.write(line)
                continue
            name, value, comment = m.groups()
            value = producers[name](value)
            print(comment + '(%s):' % value, flush=True)
            new_value = input('> ') or value
            new_file.write("%s = '%s'  # $%s\n" % (name, new_value, comment))
    remove(raw_path)
    rename(new_path, raw_path)
    exit(0)


def immediate(*args, **kwargs):
    """execute function immediately"""
    def decorate(fn):
        fn(*args, **kwargs)
    return decorate


@immediate()
def _environ_variables():
    global APP_ROOT  # 应用根路径
    global SECRET_KEY  # 全局密钥
    global DB_CONNECT  # 数据库连接
    global ALI_SMS_ACCESS    # 阿里短信服务KeyId与Secret
    global ALI_SMS_SIGN      # 阿里短信服务签名
    global ALI_SMS_TEMPLATE  # 阿里短信服务模板ID

    from os import environ

    APP_ROOT = environ.get('APP_ROOT', '/%s/%s' % (NAME, VERSION))

    SECRET_KEY = environ.get('SECRET_KEY', 'SECRET_KEY')
    # mysql+pymysql://{{account}}:{{password}}@{{serverIp}}:{{port}}/{{dbName}}?charset={{charset}}
    DB_CONNECT = environ.get('DB_CONNECT', 'sqlite:///.%s.db' % NAME)

    ALI_SMS_ACCESS = environ.get(
        'ALI_SMS_ACCESS',
        'testId,testSecret',
    ).split(',')
    ALI_SMS_SIGN = environ.get('ALI_SMS_SIGN', '阿里云短信测试专用')
    ALI_SMS_TEMPLATE = environ.get('ALI_SMS_TEMPLATE', 'SMS_71390007')


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

        @property
        def error(self): return self.logger.error

        @property
        def warning(self): return self.logger.warning

        @property
        def info(self): return self.logger.info

        @property
        def debug(self): return self.logger.debug

        def inject_logger(self, logger):
            self.logger = logger

    LOGGER = Logger(type('Logger', (object,), {
        'error': print,
        'warning': print,
        'info': print,
        'debug': print,
    }))


MODULES = ['guide', 'user', 'view']
CODE_USAGE = {
    '/guide/password/reset': {
        'text': '重置密码',
        'expiry': 3 * 60,
        'cooldown': 60,
    },
    '/user/destroy': {
        'text': '销毁账号',
        'expiry': 3 * 60,
        'cooldown': 60,
    },
}
SOCKETIO = True
