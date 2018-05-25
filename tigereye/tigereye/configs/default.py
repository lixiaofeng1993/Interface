import os


class DefaultConfig(object):

    DEBUG = True

    BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')

    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    # 数据库地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/tigereye'
    # 关闭警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 打印出所有的SQL语句
    SQLALCHEMY_ECHO = True