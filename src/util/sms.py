# -*- coding: utf-8 -*-

"""
短信工具
"""

from datetime import datetime
from uuid import uuid1
from urllib import parse
import hmac
import hashlib
from base64 import b64encode
from json import dumps

from requests import get


def send_sms(*args, **kwargs):
    q = query(params(*args, **kwargs))
    s = sign(q)
    r = request(s, q)
    return get(r)


def init_access(key_id, secret):
    global access_key_id
    global access_secret
    access_key_id = key_id
    access_secret = secret


def params(
    phone_numbers,      # 短信接收号码,支持以逗号分隔的形式进行批量调用
    sign_name,          # 短信签名
    template_code,      # 短信模板ID
    template_param,     # 短信模板变量替换JSON
    out_id='',          # 外部流水扩展字段
):
    return (
        'AccessKeyId', access_key_id,
        'Timestamp', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S%Z'),
        'Format', "JSON",
        'SignatureMethod', "HMAC-SHA1",
        'SignatureVersion', "1.0",
        'SignatureNonce', str(uuid1()),
    ) + (
        'Action', 'SendSms',
        'Version', '2017-05-25',
        'RegionId', 'cn-hangzhou',
    ) + (
        'PhoneNumbers', phone_numbers,
        'SignName', sign_name,
        'TemplateCode', template_code,
        'TemplateParam', dumps(template_param),
        'OutId', out_id,
    )


def query(params):
    i = iter(params)
    param_list = sorted(zip(i, i), key=lambda i: i[0])
    return parse.urlencode(param_list, safe='~', quote_via=parse.quote)


def sign(query):
    pre_sign = (
        'GET' + '&' + '%2F' + '&' +
                parse.quote(query, safe='~')
    )
    h = hmac.new(
        (access_secret + '&').encode('utf-8'),
        pre_sign.encode('utf-8'),
        hashlib.sha1,
    )
    return b64encode(h.digest()).decode('utf-8')


def request(sign, query):
    return 'http://dysmsapi.aliyuncs.com/?Signature=%s&%s' % (
        parse.quote(sign, safe='~'),
        query,
    )
