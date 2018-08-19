# coding:utf-8
import time
import unittest
import ddt  # 数据驱动
import os
import requests
from common import base_api
from common import readExcel
from common import writeExcel
from common.logger import Log
from common.processingJson import write_headers
# from common.connectMySql import SqL
# from common.interface_login import login

now = time.strftime('%Y-%m-%d %H-%M-%S')
# windows   拼接excel路径 用例，结果
excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data' + '\\demo_api.xlsx'
report_excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\report'
# linux
# excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/data' + '/demo_api.xlsx'
# report_excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/report'
report_xlsx = os.path.join(report_excel_path, now + 'result.xlsx')
test_data = readExcel.ExcelUtil(excel_path).dict_data()


@ddt.ddt
class Test_api(unittest.TestCase):
    """
    测试类
    """

    @classmethod  # 类方法,在所有用例前执行一次
    def setUpClass(cls):
        # cls.sql = SqL()
        cls.log = Log()
        # cls.cookies = login()  # 获取登录时需要的cookies
        cls.s = requests.session()
        # cls.s.cookies = cls.cookies  # 登录保持
        writeExcel.copy_excel(excel_path, report_xlsx)  # 复制excel文本

    @ddt.data(*test_data)
    def test_api(self, data):
        """接口测试用例"""
        res = base_api.send_requests(self.s, data)  # 调用send_requests方法,请求接口,返回结果
        if res:  # 跳过用例执行
            base_api.write_result(res, filename=report_xlsx)  # 结果写入report_path中的excel
            check = data["checkpoint"]  # 检查点 checkpoint
            self.log.info("检查点->：%s" % check)
            res_text = res["text"]  # 返回结果
            self.log.info("返回实际结果->：%s" % res_text)
            self.assertTrue(check in res_text, '检查点验证失败！')  # 断言
            self.log.info('{} {} 接口， 执行成功 ! \n'.format(data['id'], data['name']))

    @classmethod
    def tearDownClass(cls):
        # cls.sql.execute_sql('delete from project where project_name like "test%"')
        # cls.sql.execute_sql('delete from stage where stage_name like "test%"')
        # cls.sql.execute_sql('delete from `work` where work_name like "test%" or work_name = ""')
        # cls.sql.execute_sql('delete from task where task_name like "test%"')
        write_headers({})  # 清空依赖数据
        cls.log.info('测试环境恢复成功！')


if __name__ == "__main__":
    unittest.main()
