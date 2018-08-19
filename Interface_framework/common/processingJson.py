import json
import os
# from common.connectDB import SqL
from common.logger import Log
from jsonpath_rw import jsonpath, parse


# sql = SqL()

json_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\data.json'
res_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\res.json'
rely_on_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\rely_on.json'

# json_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/data' + '/data.json'


def get_json(path, field=''):
    """获取json文件中的值，data.json和res.json可共用"""
    with open(path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        if field:
            data = json_data.get(field)
            return data
        else:
            return json_data


def analysis_json(res, filed):
    """解析请求返回的json数据，返回依赖的字段和值组成的字典"""
    if isinstance(res, dict):
        if filed:
            jsonpath_expr = parse(filed)
            male = jsonpath_expr.find(res)
            value_list = [match.value for match in male]
            for value in value_list:
                data_dict = {filed: value}
                return data_dict
        else:
            Log().error('{}传入字段异常！'.format(analysis_json.__name__))
    else:
        Log().error('{} 参数不是字典类型'.format(analysis_json.__name__))


def write_body(res, field):
    """请求返回值写入data.json中，在body参数中使用。data.json中要提前写入需要的字段，然后用从返回值中提取的结果替换"""
    if isinstance(res, dict):
        if field:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                for key in json_data:
                    if isinstance(json_data[key], dict):
                        for k in json_data[key]:
                            if k == field:
                                json_data[key][field] = res[field]
                                with open(json_path, 'w', encoding='utf-8') as fp:
                                    fp.write(str(json_data).replace("'", '"'))
                                Log().info('请求返回值写入json成功！field ==> {}'.format(field))
        else:
            Log().error('{}传入字段异常！'.format(analysis_json.__name__))
    else:
        Log().error('{} 参数不是字典类型'.format(write_body.__name__))


def write_headers(res):
    """请求返回值写入token.json中，在headers中使用"""
    if isinstance(res, dict):
        with open(rely_on_path, 'w', encoding='utf-8') as f:
            json.dump(res, f)
            Log().info('依赖数据写入json文件成功！ {}'.format(res))
    else:
        Log().info('{} 参数不是字典类型'.format(write_headers.__name__))


if __name__ == '__main__':
    # body = get_json(json_path, 'registered_member')
    # print(body)
    # for k, v in body.items():
    #     print(k,v)
    # data = {'uid': 99, 'ukey': 'bef0246cb2059d90c5e4af8accdf4429'}
    # write_headers(data)
    data = get_json(res_path)
    print(data)