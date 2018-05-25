from tigereye.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_DATABASE_URI = ''

    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_SERVER_EMAIL = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    EMAIL_USE_SSL = True
    ADMINS = ['guye@iguye.com']