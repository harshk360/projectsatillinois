import os

class BaseConfig(object):
    os.environ['DEBUG'] = "True"
    if os.environ['DEBUG'] is "True":
        DEBUG = True
        SECRET_KEY = "foobarbaz"
        DB_NAME = "projects"
        DB_USER = "mysql"
        DB_PASS = "mysql"
        MYSQL_ROOT_PASSWORD = "mysql"
        DB_HOST = "localhost"
        DB_PORT = "3306"
        SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
        )
        FACEBOOK_APP_ID = "1465734760385892"
        FACEBOOK_APP_SECRET = "4e7ccd1c2b9c1a9e205a0b45051f640d"
        HOST = "localhost"
        PORT = 9001
    else:
        SECRET_KEY = os.environ['SECRET_KEY']
        DEBUG = os.environ['DEBUG']
        DB_NAME = os.environ['MYSQL_DATABASE']
        DB_USER = os.environ['MYSQL_USER']
        DB_PASS = os.environ['MYSQL_PASSWORD']
        DB_HOST = os.environ['DB_HOST']
        DB_PORT = os.environ['DB_PORT']
        SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
        )
        FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
        FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']
        HOST = "localhost"
        PORT = 80
