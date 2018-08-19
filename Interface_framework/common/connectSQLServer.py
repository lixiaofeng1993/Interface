import pymssql
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
            self.conn = pymssql.connect(host=readConfig.SQLServer_host, user=readConfig.SQLServer_user,
                                        password=readConfig.SQLServer_pwd, port=readConfig.SQLServer_port,
                                        database='sharebuy_test', charset='utf8')
            self.log.info('数据库连接成功')
        except Exception as e:
            self.log.error('数据库链接异常! {}'.format(e))

    def execute_sql(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.conn.cursor()
        with cur as cur:
            try:
                cur.execute(sql)
            except Exception as e:
                self.log.error('执行SQL语句出现异常：{}'.format(e))
                return False
            else:
                if 'select' in sql:  # 查询
                    resList = cur.fetchall()
                    return resList
                else:
                    self.conn.commit()


# def decimal_format(self, money):
#     """改变数据库数据编码格式"""
#     pay_money = Decimal(money).quantize(Decimal('0.00'))
#     return pay_money


if __name__ == '__main__':
    r = SqL()
    sql = "select user_id, all_score from score_tbl where user_id = '1022';"
    data = r.execute_sql(sql)
    for (id, NickName) in data:
        print(str(id), NickName)
