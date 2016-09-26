# -*- coding: utf-8 -*-

"""
辅助模块
"""

from flask import json, url_for


def make_resp(body, then=None, then_param=None):
    """创建响应"""
    then_param = then_param or {}
    return json.dumps(
        {
            'flag': True, 'body': body,
            'then': then and url_for(then, **then_param)
        }
    ), 200, {'Content-Type': 'application/json'}


def make_err(reas, then=None, status=403, then_param=None):
    """创建响应"""
    then_param = then_param or {}
    return json.dumps(
        {
            'flag': False, 'reas': reas,
            'then': then and url_for(then, **then_param)
        }
    ), status, {'Content-Type': 'application/json'}
