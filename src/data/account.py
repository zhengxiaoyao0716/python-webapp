#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
账户
@author: zhengxiaoyao0716
"""

from json import loads, dumps
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import \
    TimedJSONWebSignatureSerializer as Serializer, \
    SignatureExpired, BadSignature

from project import SECRET_KEY
from .base import (
    DB, Base,
    Column, Integer, String,
    or_, ForeignKey,
)


class User(Base):
    """账户"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    account = Column(String(25), unique=True, nullable=False)
    secret = Column(String(255))
    name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(25), unique=True)

    def __init__(self, account, password, name, email=None, phone=None):
        self.account = account
        password and self.set_password(password)
        self.name = name or account
        self.email = email
        self.phone = phone

    def create_token(self, expiration=3 * 24 * 60 * 60):
        """生成token"""
        serializer = Serializer(SECRET_KEY, expires_in=expiration)
        data = {'id': self.id, 'secret': self.secret[-1:-7:-1]}
        return serializer.dumps(data).decode('utf-8')

    @classmethod
    def parse_token(cls, token):
        """解析token"""
        serializer = Serializer(SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        if not data:
            return None
        self = cls.query.get(data['id'])
        return self.secret[-1:-7:-1] == data['secret'] and self

    def set_password(self, password):
        """设置密码"""
        self.secret = pwd_context.encrypt(password)

    def check_password(self, password):
        """检查密码，return error"""
        if self.secret is None:
            return u'帐号未激活'
        if not pwd_context.verify(password, self.secret):
            return u'密码错误'

    def change_password(self, old_passwd, new_passwd):
        """修改密码，return error"""
        err = self.check_password(old_passwd)
        if err:
            return err
        self.set_password(new_passwd)

    @classmethod
    def login(cls, account, password, token=''):
        """
        登入
        :return user, error
        """
        if account and password:
            self = cls.query.filter(or_(
                cls.account == account,
                cls.email == account,
                cls.phone == account,
            )).one_or_none()
            if not self:
                return None, u'帐号不存在'
            err = self.check_password(password)
            if err:
                return None, err
        else:
            if not token:
                return None, u'缺少参数'
            self = cls.parse_token(token)
            if not self:
                return None, u'token无效或已过期'
        return self, None

    @classmethod
    def search(cls, keyword):
        """查找用户（精确查询）"""
        return cls.query \
            .filter(or_(
                cls.account == keyword,
                cls.name == keyword,
                cls.phone == keyword,
                cls.email == keyword,
            )).all()

    def simple(self):
        """字典化"""
        return {
            'id': self.id,
            'account': self.account,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

    def extend(self, data=None):
        extend = UserExtend.query.filter(
            UserExtend.user_id == self.id
        ).one_or_none()
        if data is None:
            return extend.data if extend else {}
        if not extend:
            extend = UserExtend.append(self.id, data)
        else:
            extend.data = data

    def destroy(self):
        """
        销毁帐号
        请不要试图进行复杂的级联配置，
        所有与帐号关联字段应当显式的销毁
        """
        UserExtend.query.filter(UserExtend.user_id == self.id).delete()
        DB.session.delete(self)


class UserExtend(Base):
    """用户附加信息"""
    __tablename__ = 'user_extend'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    _data = Column(String, nullable=False)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

    @property
    def data(self):
        return loads(self._data)

    @data.setter
    def data(self, data):
        self._data = dumps(data)
