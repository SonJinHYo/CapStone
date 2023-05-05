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

DEBUG = True

STORAGES = {
    "default": {"BACKEND": "config.storages.MediaStorage"},
    "staticfiles":{"BACKEND": "config.storages.StaticStorage"},
    }

# static
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'quit-board-bucket'
AWS_STATIC_LOCATION = 'static'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_DEFAULT_ACL = 'public-read'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# media
MEDIA_URL = '/media/'
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR, 'media'),
]


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
