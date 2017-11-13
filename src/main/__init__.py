# -*- coding: utf-8 -*-

"""
flask server
"""

from flask import Flask, request, g

from project import (
    immediate,
    APP_ROOT, SECRET_KEY,
    MODULES, SOCKETIO,
    DB, LOGGER
)

app = Flask(__name__)
app.template_folder = '../html'
app.static_folder = '../html/static'
app.config.update(
    SECRET_KEY=SECRET_KEY,
    APPLICATION_ROOT=APP_ROOT + '/',
    SESSION_COOKIE_PATH='/',
)
LOGGER.set_logger(app.logger)


@app.before_request
def bind_data():
    """绑定请求数据"""
    g.data = request.json or request.form or request.args


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    """请求结束时或者应用关闭时删除数据库会话"""
    try:
        if not response_or_exc:
            DB.session.commit()
    finally:
        DB.session.remove()
    return response_or_exc


@immediate(*MODULES)
def _reg_blueprints(*names):
    """注册蓝图"""
    for name in names:
        main = __import__('main.blueprint.' + name)
        bp = main.blueprint.__dict__[name].blueprint
        bp.static_folder = '../../html/static'
        app.register_blueprint(
            bp, url_prefix='%s/%s' % (APP_ROOT, name))


@immediate()
def _reg_socketio():
    """注入socketio"""
    if not SOCKETIO:
        return
    from main.socket import socketio
    socketio.init_app(app, path=APP_ROOT + '/socket.io')
