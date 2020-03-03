import requests
import json

from MxOnline.settings import APIKEY


def send_captcha(apikey, mobile, andom):
    """
    :param andom:  验证码
    :param mobile:  # 手机号码
    :param text: 　＃　发送内容与云片网模板内容相同
    :return: －－返回一个dict数据
    """
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = "【任磊test】您的验证码是%s。如非本人操作，请忽略本短信" % andom
    data = {
        'apikey': apikey,
        'mobile': mobile,
        'text': text,
    }
    # 发送请求
    # res = requests.post(url, data=data)
    # return json.loads(res.text)
    ret_test = {'http_status_code': 400, 'code': 0, 'msg': '发送成功', 'detail': '参数 mobile 格式不正确，mobile:15561245'}
    return ret_test


if __name__ == "__main__":
    text = "【任磊test】您的验证码是%s。如非本人操作，请忽略本短信" % 2598
    res = send_captcha(APIKEY, 15561245, text)
    print(type(res))
    print(res)
    code = res['code']

    print(code)
