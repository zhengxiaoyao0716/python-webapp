# -*- coding: utf-8 -*-

"""
接口蓝图
"""

import datetime
from flask import Blueprint, jsonify

from project import LOGGER

blueprint = Blueprint('api', __name__)


@blueprint.before_request
def before_request():
    """请求预处理"""
    pass


@blueprint.route('/time/pull')
def pull_time():
    """拉取当前时间"""
    if False:
        return "Error reason."
    now = str(datetime.datetime.now())
    LOGGER.info('/api/time/pull %s', now)
    return jsonify({'now': now})
