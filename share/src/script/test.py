# -*- coding: utf-8 -*-

"""
调试运行
"""

import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from config import CONNECT_URL
CONNECT_URL['now'] = CONNECT_URL['test']

import webbrowser

from dao import drop_all, create_all, db_session
from dao.model import *
from main import app


def init_test_data():
    """初始化测试数据"""
    drop_all()
    create_all()
    db_session.commit()

if __name__ == '__main__':
    app.config.from_object('main.config.DevelopConfig')
    init_test_data()

    @app.before_request
    def add_debug_ctx():
        """添加调试上下文"""
        pass
    webbrowser.open('http://localhost:5000/{{appId}}/view')
    app.run(host='0.0.0.0')
