# -*- coding: utf-8 -*-

"""
辅助工具
"""

import random
from string import ascii_uppercase, digits
from datetime import timedelta, datetime


def rand_code(size=6, chars=ascii_uppercase + digits):
    return ''.join(random.sample(chars, 6))


def get_time(day=0, second=0):
    """获取时间"""
    return str(datetime.now() + timedelta(day, second))[0:19]
