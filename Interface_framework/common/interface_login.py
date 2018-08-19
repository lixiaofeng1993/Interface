import os
import requests
import json
from common import readConfig
from common.logger import Log
from common.processingJson import write_headers, write_body, analysis_json

log = Log()


def login():
    """获取保持登录的cookies，保存token值到json文件"""
    res = requests.post(readConfig.url, data={"userNo": readConfig.username, "password": readConfig.password})
    assert '{"user":{"roleIds":' in res.text
    log.info('用户登录成功！')
    if 'token' in res.text:
        data = json.loads(res.text)  # 返回值有null的话，需要使用loads转成dict
        token_dict = analysis_json(data, 'token')
        write_body(token_dict, 'token')
    return res.cookies


if __name__ == '__main__':
    login()
