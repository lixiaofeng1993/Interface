import pymysql
# from decimal import Decimal
import time

from common.logger import Log
from common import readConfig


class SqL:
    """
    连接数据库封装

    """

    def __init__(self):
        self.log = Log()
        """判断是否连接成功"""
        try:
            self.conn = pymysql.connect(host=readConfig.MySQL_host, database=readConfig.MySQL_database, user=readConfig.MySQL_user,
                                        password=readConfig.MySQL_pwd, port=int(readConfig.MySQL_port), charset='utf8')
            self.log.info('数据库连接成功')
        except Exception as e:
            self.log.error('数据库链接异常! {}'.format(e))

    def execute_sql(self, sql, dict_type=False, num=1):
        """返回查询结果集
            sql: 执行的sql语句；
            dict_type: 是否返回的数据是字典类型；
            num： 返回的数据是一个还是多个
        """
        if dict_type:  # 返回数据字典类型
            cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        else:
            cur = self.conn.cursor()
        try:
            with cur as cur:
                cur.execute(sql)  # 执行sql
            if 'delete' in sql:
                self.conn.commit()  # 提交
            else:
                if num == 1:  # 返回一条数据
                    data = cur.fetchone()
                    if dict_type:
                        return data
                    else:
                        return data[0]
                else:  # 返回多条数据
                    data_str = ''
                    data = cur.fetchall()
                    if dict_type:
                        return data
                    else:
                        for i in data:
                            for j in i:
                                data_str += str(j) + ','  # 拼接返回数据
                        return data_str
        except Exception as e:
            self.conn.rollback()
            self.log.error('执行SQL语句出现异常：{}'.format(e))
            return None

    def __del__(self):
        self.conn.close()


# def decimal_format(self, money):
#     """改变数据库数据编码格式"""
#     pay_money = Decimal(money).quantize(Decimal('0.00'))
#     return pay_money


if __name__ == '__main__':
    r = SqL()
    data = r.execute_sql("select ct.unionid from customer_tbl as ct where ct.nickname = 'Smithereens。';")
    print(data)
    print(type(data))