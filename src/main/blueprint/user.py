# -*- coding: utf-8 -*-

"""
用户
"""

from flask import Blueprint, g, session, make_response, jsonify

from data import User
from util import check_code

blueprint = Blueprint('user', __name__)


@blueprint.before_request
def before_request():
    """请求预处理"""
    if 'user' in session:
        user = User.query.get(session['user'])
        if not user:
            return u'身份过期，请重新登录', 401
        g.user = user
    else:
        return u'请先登录', 401


@blueprint.route('/logout')
def logout():
    """登出"""
    session.pop('user')
    resp = make_response('fin')
    resp.delete_cookie('user')
    return resp


@blueprint.route('/destroy', methods=['POST'])
def destroy():
    """销毁账号"""
    err = check_code(g.user, '/user/destroy', g.data['code'])
    if err:
        return err, 403
    err = g.user.destroy()
    if err:
        return err, 403
    return logout()


@blueprint.route('/password/update', methods=['POST'])
def update_password():
    """修改密码"""
    err = g.user.change_password(
        g.data['old'], g.data['new'])
    if err:
        return err, 403
    return logout()


@blueprint.route('/user/search')
def search_user():
    """查询用户"""
    return jsonify([user.simple() for user in User.search(g.data['keyword'])])
