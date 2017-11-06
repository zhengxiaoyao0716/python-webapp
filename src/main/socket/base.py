# -*- coding: utf-8 -*-

from functools import wraps
from flask_socketio import SocketIO
from flask import request, session, json

from project import DB, LOGGER
from data import User
from util import get_time

socketio = SocketIO()


def use_namespace(namespace):
    """注入命名空间"""
    def on(message):
        return socketio.on(message, namespace=namespace)
    return on


on = use_namespace('/socket')


def db_session(fn):
    """数据库连接装饰器"""
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        r = fn(*args, **kwargs)
        try:
            DB.session.commit()
        finally:
            DB.session.remove()
        return r
    return _wrapper


def with_login(fn):
    """登录状态装饰器"""
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        if 'user' in session:
            user = User.query.get(session['user'])
            if not user:
                return False, '身份过期，请重新登录'
        else:
            user, err = User.login(
                None, None, request.cookies.get('user'))
            if err:
                return False, '自动登录失败，' + err
        return fn(user, *args, **kwargs)
    return _wrapper


@on('connect')
def connect():
    LOGGER.info('connected')


@on('disconnect')
def disconnect():
    LOGGER.info('disconnected')


@on('message')
def message(message):
    LOGGER.info('message: %s', message)
    return message


@on('/guide/time/pull')
def pull_time():
    return json.dumps({'now': get_time()})


@on('/user/user/search')
@with_login
@db_session
def search_user(user, data):
    return json.dumps([user.simple() for user in User.search(data['keyword'])])
