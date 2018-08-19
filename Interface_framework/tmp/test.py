import requests
import json
#
# headers = {"unionid": "oPmunjjIzQtjk2aBI4pfkVLcA9tE"}
# data = {
#     "Content-Type": "application/json",
#     "channel": "SHOP",
#     "uid": "9",
#     "ukey": "f07796b0cc0295b212ecbdb93843a95a"
#   }
#
# print(type(data))
# url = 'http://dev.sign.xxbmm.com/customers/account'
# s = requests.session()
# res = s.request(method='get', data=headers, headers=data, verify=False, params=None, url=url)
# print(res.text)
# print(res.cookies)

# data = {"channel": "SHOP", "uid": 9, "ukey": "f07796b0cc0295b212ecbdb93843a95a"}
# headers = {"Content-Type": "application/json"}
# r = {}
# r.update(data)
# r.update(headers)
# print(r)
# url = 'http://dev.sign.xxbmm.com/customers'
#
# data = {
#         "unionid": "1"
#     }
#
# # data["param"] = json.dumps({
# #         "unionid": "2kds99ksdSD7F3b"
# #     })
# headers={"Content-Type": "application/json"}
# s = requests.session()
# res = s.request(method='post', data=json.dumps(data), headers=headers, verify=False, params=None, url=url)
# # res = requests.post(url=url, data=json.dumps(data), headers={"Content-Type": "application/json"}, verify=False)
# print(res.content.decode("utf-8"))

# data = '{"suc":true,"msg":"成功","error_code":10001,"data":{"uid":99,"ukey":"bef0246cb2059d90c5e4af8accdf4429"}}'
# d = json.loads(data)
# print(type(d))
# print(json.loads(data)['data'])
#
# headers = {"unionid": "oPmunjjIzQtjk2aBI4pfkVLcA9tE", "gold": "121199210"}
# data = {
#     "Content-Type": "application/json",
#     "channel": "SHOP",
#     "uid": "9",
#     "ukey": "f07796b0cc0295b212ecbdb93843a95a"
#   }
#
# print(type(data))
# url = 'http://dev.sign.xxbmm.com/customers/account/gold'
# s = requests.session()
# res = s.request(method='delete', params=headers, headers=data, verify=False, data=None, url=url)
# print(res.text)
# print(res.cookies)


#
# data = {
#   "gold": 121199210,
#   "unionid": "asdasd2223a"
# }
# headers = {
#     "Content-Type": "application/json",
#     "channel": "SHOP",
#     "uid": "9",
#     "ukey": "f07796b0cc0295b212ecbdb93843a95a"
#   }
#
# print(type(data))
# url = 'http://dev.sign.xxbmm.com/customers/account/gold'
# s = requests.session()
# res = s.request(method='put', params=None, headers=headers, verify=False, data=json.dumps(data), url=url)
# print(res.text)
# print(res.cookies)


# data = {
#     "gold": 1,
#     "unionid": ""
#   }
# headers = {
#     "Content-Type": "application/json",
#     "channel": "SHOP",
#     "uid": "34",
#     "ukey": "96cb11a97d34118c77f7db1b4a953b3e"
#   }
#
# print(type(data))
# url = 'http://dev.sign.xxbmm.com/customers/account/gold'
# s = requests.session()
# res = s.request(method='delete', params=json.dumps(data), headers=headers, verify=False, data=None, url=url)
# print(res.text)
# print(res.cookies)

import datetime, time
stopTime = datetime.datetime.now()
print(stopTime)
print(time.localtime())


def TimeStampToTime(timestamp):
    """格式化时间"""
    timeStruct = time.localtime(timestamp)
    return str(time.strftime('%Y-%m-%d %H:%M:%S', timeStruct))
print(TimeStampToTime(time.time()))