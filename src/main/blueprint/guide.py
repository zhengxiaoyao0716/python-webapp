# -*- coding: utf-8 -*-

"""
游客
"""

from flask import Blueprint, g, request, session, jsonify, make_response

from data import DB, User

blueprint = Blueprint('guide', __name__)


@blueprint.route('/user/login', methods=['POST'])
def login_user():
    """用户登录"""
    user, err = User.login(
        g.data.get('account'),
        g.data.get('password'),
        request.cookies.get('user'),
    )
    if err:
        return err, 403
    session['user'] = user.id
    token = user.create_token()
    user_dict = user.simple()
    user_dict['token'] = token
    resp = make_response(jsonify(user_dict))
    resp.set_cookie('user', token)
    return resp


@blueprint.route('/verify_code/get', methods=['POST'])
def get_verify_code():
    """获取验证码（副作用为创建User）"""
    account = g.data['account']
    user = User.query \
        .filter(User.account == account) \
        .one_or_none()
    email = g.data.get('email')
    phone = g.data.get('phone')

    if user:
        # 用户已存在，若邮箱或手机号能够匹配，可以尝试重置
        if not email and not phone:
            return '账号已存在，请认证邮箱或手机', 403
        if email and user.email != email:
            return '账号已存在，尝试用邮箱认证但不匹配', 403
        if phone and user.phone != phone:
            return '账号已存在，尝试用手机认证但不匹配', 403
    else:
        user = User.append(account, None, None, email=email, phone=phone)
    DB.session.flush()

    # TODO 发送验证码
    # user.set_password(code)
    if email:
        pass
    if phone:
        pass

    resp = make_response('fin')
    resp.set_cookie('verify_user', str(user.id))
    resp.set_cookie('verify_email', email or user.email)
    resp.set_cookie('verify_phone', phone or user.phone)
    return resp


@blueprint.route('/password/reset', methods=['POST'])
def reset_password():
    """重置密码（副作用可以创建User）"""
    user = User.query.get(request.cookies.get('verify_user'))
    if not user:
        return '设置密码失败，无效的cookie或已过期', 403
    # TODO 校验验证码
    # if not user.check_password(g.data['code']):
    #     return '设置密码失败，验证码无效或已过期', 403

    user.set_password(g.data['password'])
    user.email = request.cookies.get('verify_email')
    user.phone = request.cookies.get('verify_phone')

    resp = make_response('fin')
    resp.delete_cookie('verify_user')
    resp.delete_cookie('verify_email')
    resp.delete_cookie('verify_phone')
    return resp
