# -*- coding: utf-8 -*-
"""
数据库基础模板
"""

from sqlalchemy.ext.declarative import declarative_base as _base

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from dao.connect import db_session


Base = _base()
Base.query = db_session.query_property()

def _column_dict(self):
    """直接读取列字典"""
    model_dict = dict(self.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict
Base.column_dict = _column_dict
def _add_new(cls, *args, **kwargs):
    self = cls(*args, **kwargs)
    db_session.add(self)
    return self
Base.add_new = classmethod(_add_new)
