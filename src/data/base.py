# -*- coding: utf-8 -*-
"""
数据库基础模板
"""

from sqlalchemy.ext.declarative import declarative_base as _base
from sqlalchemy import (  # noqa: F401
    Column, Integer, String, Text, Boolean,
    or_, ForeignKey, Table,
)
from sqlalchemy.orm import relationship  # noqa: F401

from project import DB

Base = _base()
Base.query = DB.session.query_property()


def simple_model_dict(self):
    """获取实例字典"""
    model_dict = dict(self.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict


Base.simple = simple_model_dict
Base.__repr__ = lambda self: str(simple_model_dict(self))


def append_model_instance(cls, *args, **kwargs):
    """添加新的实例"""
    self = cls(*args, **kwargs)
    DB.session.add(self)
    return self


Base.append = classmethod(append_model_instance)
