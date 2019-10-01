from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'calendar.cju6s7rtvsvl.ap-northeast-2.rds.amazonaws.com',
        'NAME': 'roqkfwkehlwk',
        'USER': 'roqkfwkehlwk',
        'PASSWORD': 'password44',
        'PORT': '3306',
    }
}