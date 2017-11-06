# -*- coding: utf-8 -*-

"""
游客
"""

from flask import Blueprint, g, request, session, jsonify, make_response

from project import LOGGER, CODE_USAGE
from data import DB, User
from util import rand_code, get_time, check_code

blueprint = Blueprint('guide', __name__)


@blueprint.route('/time/pull')
def pull_time():
    """拉取当前时间"""
    if False:
        return "Error reason.", 403
    now = get_time()
    LOGGER.info('/api/time/pull %s', now)
    return jsonify({'now': now})


@blueprint.route('/login', methods=['POST'])
def login():
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
    """
    获取验证码
    : 若用户存在，则至少要通过邮箱或手机进行一次匹配
    : 若用户不存在，创建不可登录用户（无密码未激活）
    """
    usage = g.data.get('usage')
    conf = CODE_USAGE.get(usage)
    if conf is None:
        return 'usage参数无效: %s' % usage, 400
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

    extend = user.extend()
    _, expiry = extend \
        .pop(usage, '0,-1').split(',')
    if expiry > get_time():
        return '请求验证码过于频繁，请稍候再试', 403
    code = rand_code()
    user.extend({
        **extend,
        usage: code + ',' + get_time(second=conf['expiry']),
    })
    # TODO 发送验证码
    LOGGER.info('%s %d %s', usage, user.id, code)
    if email:
        pass
    if phone:
        pass

    return 'fin'


@blueprint.route('/password/reset', methods=['POST'])
def reset_password():
    """
    重置密码
    : 若帐号未激活，则直接设置为新密码并激活
    """
    user = User.query.filter(User.account == g.data['account']).one_or_none()
    err = check_code(user, '/guide/password/reset', g.data['code'])
    if err:
        return err, 403
    user.set_password(g.data['password'])
    return 'fin'
