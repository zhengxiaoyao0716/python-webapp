# -*- coding: utf-8 -*-

"""
数据库模块
"""

# flake8: noqa
from project import DB
from .model import *


def create_all():
    """创建所有表"""
    Base.metadata.create_all(bind=DB.engine)


def drop_all():
    """清空所有表"""
    Base.metadata.drop_all(bind=DB.engine)
