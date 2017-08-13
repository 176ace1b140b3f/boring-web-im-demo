class DevelopmentConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/web-im-dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'notsecretatall'
