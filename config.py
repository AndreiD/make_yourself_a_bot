import os

basedir = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


class Config(object):
    ADMIN_EMAIL = "your_email@your_company.com"

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    APP_NAME = 'XResume'
    SECRET_KEY = 'secret_here'
    LISTINGS_PER_PAGE = 5

    SECURITY_REGISTERABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt_123_hard_one'
    SECURITY_CONFIRMABLE = False

    RECAPTCHA_SITE_KEY = "6Ld55CkTAAAAAK_xxxxxxxxxxxxxxx"
    RECAPTCHA_SECRET = "6Ld55CkTAAAAALf5j_xxxxxxxxxxxxxxx"


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_db_user:password@localhost:3306/database'
    DEBUG = True


