# -*- coding: utf-8 -*-

"""
调试运行
"""

import os
from requests import session
os.sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


def init_test_data():
    print('', flush=True)
    print('INIT_TEST_DATA:', flush=True)

    from data import User
    drop_all()
    create_all()
    u = User.append('zheng', 'password', '正逍遥0716', phone='18101301995')
    DB.session.flush()
    u.extend({'manager': True})
    DB.session.commit()
    print(u.simple(), u.extend(), flush=True)

    print('', flush=True)


if __name__ == '__main__':
    import webbrowser
    from project import APP_ROOT, SOCKETIO, DB
    from main import app, g
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
        g.debug = True
    webbrowser.open('http://localhost:5000%s/view' % APP_ROOT, new=0)
    if SOCKETIO:
        from main.socket import socketio
        socketio.run(app, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')


def init_requests():
    from project import APP_ROOT
    API = 'http://localhost:5000' + APP_ROOT
    self = session()
    global get
    global post

    def request(method, url, *args, **kwargs):
        r = self._request(method, API + url, *args, **kwargs)
        if not r.ok:
            print(r.reason, r.text, flush=True)
        return r
    self._request, self.request = self.request, request
    get, post = self.get, self.post
    return get, post


def get_verify_code(usage, account, email=None, phone=None):
    return post('/guide/verify_code/get', json={
        'usage': usage, 'account': account, 'email': email, 'phone': phone})


def test_verify():
    account = 'test_verify'
    phone = '12312341234'

    usage = '/guide/password/reset'
    get_verify_code(usage, account, phone=phone)
    code = input('code:')
    post(usage, {'account': account, 'code': code, 'password': 'password'})

    usage = '/user/destroy'
    get_verify_code(usage, account, phone=phone)
    post('/guide/login',
         {'account': account, 'password': 'password'})
    code = input('code:')
    post(usage, {'code': code})


def test_user():
    post('/guide/login',
         {'account': 'zheng', 'password': 'password'})
    post('/user/password/update',
         {'old': 'password', 'new': 'password'})
    post('/guide/login',
         {'account': 'zheng', 'password': 'password'})
    print(get('/user/user/search?keyword=zheng').json())
    print('')

    get('/user/logout')
