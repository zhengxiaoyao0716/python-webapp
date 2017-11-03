# -*- coding: utf-8 -*-

"""
调试运行
"""

import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


def init_test_data():
    from data import User
    drop_all()
    create_all()
    u = User.append('zheng', 'password', '正逍遥0716', phone='18101301995')
    DB.session.flush()
    u.extend({'manager': True})
    DB.session.commit()
    print(u.simple(), flush=True)


if __name__ == '__main__':
    import webbrowser
    from flask import session  # flake8: noqa

    from project import NAME, DB
    from main import app
    from data import drop_all, create_all

    init_test_data()

    app.config.update(
        DEBUG=True,
        PORT=5000,
    )

    @app.before_request
    def add_debug_ctx():
        """添加调试上下文"""
        # session['user'] = 1
    webbrowser.open('http://localhost:5000/%s/view' % NAME)
    app.run(host='0.0.0.0')
