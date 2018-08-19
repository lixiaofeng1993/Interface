# coding:utf-8
import os
import json
import random
import requests
from common.readExcel import ExcelUtil
from common.writeExcel import Write_excel
from common.logger import Log
from common.processingJson import get_json, write_headers
from common.connectMySql import SqL
from common import readConfig

log = Log()
sql = SqL()

json_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\data.json'
res_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\res.json'
rely_on_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\rely_on.json'
last_id = ""


def send_requests(s, data_dict):
    """封装requests请求"""
    if not isinstance(data_dict, dict):  # 判断传入参数类型
        raise TypeError('{} 参数不是字典类型'.format(send_requests.__name__))
    if data_dict['skip'] == 'true':  # 判断测试数据是否执行.在excel中打标记，为true则不执行。不输入或其他值，继续执行
        log.info('{} {} 接口 用例 不执行'.format(data_dict['id'], data_dict['name']))
        return False
    else:
        method = data_dict["method"]  # 获取请求方式
        url = data_dict["url"]  # 获取请求地址
        type = data_dict["type"]  # 请求参数类型
        test_nub = data_dict['id']  # 测试用例id
        test_name = data_dict['name']  # 测试用例中文名称

        # 判断参数 params
        try:
            params = eval(data_dict["params"])  # 如果 params 有值 ，则转换成字典类型
        except:
            params = None  # 报错则赋值 None

        # 判断headers     yes 读取 res.json 中的数据      no 不执行
        headers = get_json(res_path)
        rely_on = get_json(rely_on_path)  # 取出保存的返回数据
        if data_dict["headers"] == 'yes':
            for k, v in headers.items():
                if k in ['uid', 'ukey']:
                    if rely_on != {}:
                        if isinstance(rely_on[k], int):  # 替换返回数据中的int类型
                            rely_on[k] = str(rely_on[k])
                        headers[k] = rely_on[k]
        else:
            headers = None

        # 判断body
        try:
            body_data = eval(data_dict["body"])  # 如果 body 有值，则转换成字典类型
        except:
            body_data = {}  # 报错则赋值 空字典
        # 判断body数据类型
        if type == "data":  # data  取excel中的body数据
            body = body_data
        elif type == "json":  # json  取data.json中的body数据， 默认字典类型
            body = get_json(json_path, data_dict['body'])
            random_id = random.randint(1, 10000000)
            for k, v in body.items():
                if k == 'unionid' or 'content_id':
                    if data_dict["make"] == 'true':
                        if k == 'content_id':
                            if data_dict['params'] == 'true':
                                pass
                            else:
                                global last_id
                                body[k] = last_id
                    else:
                        if k == 'unionid':
                            body[k] = readConfig.unionid
                        if k == 'content_id':
                            body[k] = random_id
                            last_id = random_id
        elif type == "sql":  # sql  取data.json中的body数据，如果是查询语句，则执行查询数据库操作，并把返回的值重新赋值给参数
            # make = False  # 标记，body数据类型 list or dict
            body = get_json(json_path, data_dict['body'])
            # if isinstance(body, list):  # 对于参数是list的情况，需要把list遍历成dict后重新赋值
            #     make = True
            #     for b_dict in body:
            #         body = b_dict
            if isinstance(body, dict):
                for k, v in body.items():
                    if isinstance(v, int):  # 把值转为字符串   <不转会报错，对于 headers 为 yes 时>
                        v = str(v)
                    if 'select' in v:
                        log.info('从数据库中查数据的sql是： {}'.format(v))
                        date = sql.execute_sql(v)
                        # if date is None:  # 阶段id 无法查询报错， 返回 None ，重新查询一次
                        #     date = sql.execute_sql('select id from stage order by id desc limit 1;')
                        body[k] = date

                        # if make:  # make 为 true，表示参数的初始类型为list，替换value后，需要重新转换为list类型
                        #     body = [body]
        else:
            body = body_data
        if data_dict["headers"] == 'yes':  # headers 为 yes 时， body数据需要转为字符串类型
            body = json.dumps(body)

        # if method in ['delete', 'get']:  # 除post请求外，其他默认传参数 params 。处理其他请求需要传参数的情况
        if method == 'get':  # 除post请求外，其他默认传参数 params 。处理其他请求需要传参数的情况
            params = body
            if data_dict['params'] == 'true':  # 区别 params 参数传参，json字符串 or dict
                pass
            else:
                params = json.loads(params)  # 获取冻结明细
            body = None

        log.info("*******正在执行用例：-----  {} {}  ----**********".format(test_nub, test_name))
        log.info("请求方式： {}, 请求url: {}".format(method, url))
        log.info("请求params：{}".format(params))
        log.info("请求头部：{}".format(headers))
        if method in ["post", "put", "delete"]:
            log.info("{} 请求body类型为：{} ,body内容为 {}".format(method, type, body))

        verify = False  # 证书认证
        res = {}  # 接受返回数据
        try:
            # 构造请求
            r = s.request(method=method,
                          url=url,
                          params=params,
                          headers=headers,
                          data=body,
                          verify=verify,
                          )
            log.info("页面返回信息：%s" % r.content.decode("utf-8"))
            # 信息存储到res字典中
            res['id'] = data_dict['id']
            res['rowNum'] = data_dict['rowNum']
            res['name'] = data_dict['name']
            res["status_code"] = str(r.status_code)  # 状态码转成str
            res["text"] = r.content.decode("utf-8")
            res['return_code'] = str(json.loads(res['text'])['error_code'])  # 获取系统返回状态码
            res["times"] = str(r.elapsed.total_seconds())  # 接口请求时间转str

            if res["status_code"] != "200":  # 判断返回code是否正常
                res["error"] = res["text"]
            else:
                res["error"] = ""
                # if data_dict["make"] == 'true':  # 如果没有返回值，判断状态码 excel中打标记，把状态码写入返回值中
                #     res["text"] = res['status_code']

            if data_dict["checkpoint"] in res["text"]:  # 断言 返回信息是否正确
                res["result"] = "pass"
                log.info("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
                if test_name == '会员登录-正常传值':
                    rely_on = json.loads(res['text'])['data']
                    write_headers(rely_on)  # 把依赖数据写入到json文件
                if '会员当天签到状态' in test_name:
                    status = json.loads(res['text'])['data']
                    log.info('会员当天签到状态是：{}'.format(status))
            else:
                res["result"] = "fail"  # 断言失败结果
            res["msg"] = ""
            return res
        except Exception as msg:
            log.error('请求出现异常！ {}'.format(msg))
            res["msg"] = str(msg)  # 出现异常，保存错误信息
            res["result"] = "error"  # 结果保存错误
            return res


def write_result(result, filename="result.xlsx"):
    row_nub = result['rowNum']  # 返回结果的行数row_nub
    # 结果写入excel中
    wt = Write_excel(filename)
    wt.write(row_nub, 9, result['status_code'])  # 写入返回状态码status_code,第8列
    wt.write(row_nub, 10, result['return_code'])  # 写入系统接口返回状态码
    wt.write(row_nub, 11, result['times'])  # 耗时
    wt.write(row_nub, 12, result['error'])  # 状态码非200时或系统状态码异常时的返回信息
    wt.write(row_nub, 14, result['result'])  # 结果
    wt.write(row_nub, 15, result['msg'])  # 抛异常


if __name__ == "__main__":
    excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/data' + '/demo_api.xlsx'
    data = ExcelUtil(excel_path).dict_data()
    s = requests.session()
    res = send_requests(s, data[4])
