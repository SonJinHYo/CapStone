from . base import *
import pymysql
import environ

pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 4, 13, "final", 0)
env = environ.Env()

ALLOWED_HOSTS = [
    "ec2-43-200-248-130.ap-northeast-2.compute.amazonaws.com",
    ".quitboard.click",
]
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # engine: mysql
        'NAME' : 'mysqlDB', # DB Name
        'USER' : 'admin', # DB User
        'PASSWORD' : env("AWS_DB_PASSWORD"), # Password
        'HOST': 'database-1.c3zb6mrofwf7.ap-northeast-2.rds.amazonaws.com', # 생성한 데이터베이스 엔드포인트
        'PORT': '3306', # 데이터베이스 포트
        'OPTIONS':{
            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


DEBUG = True