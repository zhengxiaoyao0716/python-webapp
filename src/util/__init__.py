# -*- coding: utf-8 -*-

"""
辅助工具
"""

import random
from string import ascii_uppercase, digits
from datetime import timedelta, datetime

from project import immediate
from .sms import send_sms  # noqa: F401


@immediate()
def _init_sms():
    from project import ALI_SMS_ACCESS
    from .sms import init_access
    init_access(*ALI_SMS_ACCESS)


def get_time(day=0, second=0):
    """获取时间"""
    return str(datetime.now() + timedelta(day, second))[0:19]


def rand_code(size=6, chars=ascii_uppercase + digits):
    return ''.join(random.sample(chars, 6))


def check_code(user, usage, code):
    """校验验证码，失败返回错误原因"""
    if not user:
        return '帐号不存在'
    extend = user.extend()
    _code, expiry = extend \
        .pop(usage, '0,-1').split(',')
    user.extend(extend)
    if expiry < get_time():
        return '验证码已过期'
    if code != _code:
        return '无效的验证码'
