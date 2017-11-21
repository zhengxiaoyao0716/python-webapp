import unittest

from sms import init_access, query, sign, request


class TestSms(unittest.TestCase):
    def test_request(self):
        access_key_id = 'testId'
        access_secret = 'testSecret'
        init_access(access_key_id, access_secret)

        expect = {
            'query': 'AccessKeyId=testId&Action=SendSms&Format=XML&OutId=123&PhoneNumbers=15300000001&RegionId=cn-hangzhou&SignName=%E9%98%BF%E9%87%8C%E4%BA%91%E7%9F%AD%E4%BF%A1%E6%B5%8B%E8%AF%95%E4%B8%93%E7%94%A8&SignatureMethod=HMAC-SHA1&SignatureNonce=45e25e9b-0a6f-4070-8c85-2956eda1b466&SignatureVersion=1.0&TemplateCode=SMS_71390007&TemplateParam=%7B%22customer%22%3A%22test%22%7D&Timestamp=2017-07-12T02%3A42%3A19Z&Version=2017-05-25',  # noqa: E501
            'sign': 'zJDF+Lrzhj/ThnlvIToysFRq6t4=',  # noqa: E501
            'request': 'http://dysmsapi.aliyuncs.com/?Signature=zJDF%2BLrzhj%2FThnlvIToysFRq6t4%3D&AccessKeyId=testId&Action=SendSms&Format=XML&OutId=123&PhoneNumbers=15300000001&RegionId=cn-hangzhou&SignName=%E9%98%BF%E9%87%8C%E4%BA%91%E7%9F%AD%E4%BF%A1%E6%B5%8B%E8%AF%95%E4%B8%93%E7%94%A8&SignatureMethod=HMAC-SHA1&SignatureNonce=45e25e9b-0a6f-4070-8c85-2956eda1b466&SignatureVersion=1.0&TemplateCode=SMS_71390007&TemplateParam=%7B%22customer%22%3A%22test%22%7D&Timestamp=2017-07-12T02%3A42%3A19Z&Version=2017-05-25',  # noqa: E501
        }

        params = (
            'AccessKeyId', access_key_id,
            'Timestamp', '2017-07-12T02:42:19Z',
            'Format', "XML",
            'SignatureMethod', "HMAC-SHA1",
            'SignatureVersion', "1.0",
            'SignatureNonce', '45e25e9b-0a6f-4070-8c85-2956eda1b466',
        ) + (
            'Action', 'SendSms',
            'Version', '2017-05-25',
            'RegionId', 'cn-hangzhou',
        ) + (
            'PhoneNumbers', '15300000001',
            'SignName', '阿里云短信测试专用',
            'TemplateCode', 'SMS_71390007',
            'TemplateParam', '{"customer":"test"}',
            'OutId', '123',
        )

        q = query(params)
        print(q, '\n')
        self.assertEqual(q, expect['query'])

        s = sign(q)
        print(s, '\n')
        self.assertEqual(s, expect['sign'])

        r = request(s, q)
        print(r, '\n')
        self.assertEqual(r, expect['request'])


if __name__ == '__main__':
    unittest.main()
