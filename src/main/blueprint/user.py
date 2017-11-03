# -*- coding: utf-8 -*-

"""
用户
"""

from flask import Blueprint, g, session, make_response, jsonify

from data import User

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


@blueprint.route('/password/update', methods=['POST'])
def update_password():
    """修改密码"""
    _, err = g.user.change_password(
        g.data['oldPasswd'], g.data['newPasswd'])
    if err:
        return err, 403
    return 'fin'


@blueprint.route('/user/search')
def search_user():
    """查询用户"""
    return jsonify([user.simple() for user in User.search(g.data['keyword'])])
