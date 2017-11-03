# -*- coding: utf-8 -*-

"""
调试运行
"""

import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


if __name__ == '__main__':
    import webbrowser

    from project import NAME, DB
    from dao import drop_all, create_all
    from main import app

    drop_all()
    create_all()
    DB.session.commit()

    app.config.update(
        DEBUG=True,
        PORT=5000,
    )

    @app.before_request
    def add_debug_ctx():
        """添加调试上下文"""
        pass
    webbrowser.open('http://localhost:5000/%s/view' % NAME)
    app.run(host='0.0.0.0')
