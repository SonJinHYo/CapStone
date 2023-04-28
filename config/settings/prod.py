from . base import *

ALLOWED_HOSTS = [
    "ec2-43-200-248-130.ap-northeast-2.compute.amazonaws.com",
]
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = True