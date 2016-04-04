# Copyright 2016, RadiantBlue Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django settings for alerts project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from __future__ import absolute_import

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wev&eoj^^la1pdqsa+rbb%ia*(#i07-fti99wroo^zoxu79fpp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'fulcrum_importer'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mvp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mvp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'test.sqlite3'),
        },
    },
    'fulcrum': {
    'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'fulcrum_db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'fulcrum_test.sqlite3'),
        },
    }
}


# DATABASES['default'] = {}
#
# DATABASES['fulcrum'] = {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'fulcrum_data',
#         'USER': 'admin',
#         'PASSWORD': 'geoserver',
#         'HOST': 'localhost',
#         'PORT': '5432', # Notice: string
#     }



# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'cache'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = None

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = './fulcrum_importer/static'
STATIC_URL = '/static/'

MEDIA_ROOT = r"F:\fulcrum_upload"
#MEDIA_ROOT = os.path.join(BASE_DIR,'assets')
MEDIA_URL = 'assets/'

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Name of nodes to start
# here we have a single node
# or we could have three nodes:
# CELERYD_NODES="w1 w2 w3"
#
# Absolute path to "manage.py"
# CELERY_BIN="/var/lib/demo/manage.py"
#
# CELERY_IMPORTS = ("mvp.celery","fulcrum_importer.tasks")
#
# How to call manage.py
# CELERYD_MULTI="celery multi"
#
# Extra command-line arguments to the worker
# CELERYD_OPTS="--time-limit=300 --concurrency=2"
#
# %N will be replaced with the first part of the nodename.
# CELERYD_LOG_FILE="/var/log/celery_fi/%N.log"
# CELERYD_PID_FILE="/var/run/celery/%N.pid"
#
#

DJANGO_FULCRUM_USE_CELERY = False
DJANGO_FULCRUM_DELAY = 30

# FILESERVICE_CONFIG = {
#     'store_dir': '/var/lib/geoserver_data/file-service-store',
#     # example: ('*', ) or ('.mov', '.jpg', ...),
#     'types_allowed': ('*', ),
#     # maploom will replace {} with the media item name such as 7ff194b54ab57a829094dc0afc624c78815ec02c.jpg
#     'url_template': '/api/fileservice/view/{}'
# }

CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'
CELERY_SEND_EVENTS=True
CELERYBEAT_USER='geoshape'
CELERYBEAT_GROUP='geoservice'
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'Update_layers_30_secs': {
        'task': 'fulcrum_importer.tasks.task_update_layers',
        'schedule': timedelta(seconds=30),
        'args': None
    },
   'pull_s3_data_60_secs': {
        'task': 'fulcrum_importer.tasks.pull_s3_data',
        'schedule': timedelta(seconds=60),
        'args': None
    },
}
USE_TZ = False
TIME_ZONE = None
SSL_VERIFY = False

FULCRUM_UPLOAD = '/var/lib/geonode/fulcrum_data'

# SITEURL = 'https://geoshape.dev/'
#
# GEOSERVER_URL = SITEURL + 'geoserver/'
#
# OGC_SERVER = {
#     'default' : {
#         'BACKEND' : 'geonode.geoserver',
#         'LOCATION' : GEOSERVER_URL,
#         'PUBLIC_LOCATION' : GEOSERVER_URL,
#         'USER' : 'admin',
#         'PASSWORD' : 'geoserver',
#         'MAPFISH_PRINT_ENABLED' : True,
#         'PRINT_NG_ENABLED' : True,
#         'GEONODE_SECURITY_ENABLED' : True,
#         'GEOGIG_ENABLED' : True,
#         'WMST_ENABLED' : False,
#         'DATASTORE': 'geoshape_imports',
#         'GEOGIG_DATASTORE_DIR':'/var/lib/geoserver_data/geogig',
#     }
# }


# CACHES = {
#      'default': {
#          'BACKEND':
#          'django.core.cache.backends.memcached.MemcachedCache',
#          'LOCATION': '127.0.0.1:11211',
#      }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(FULCRUM_UPLOAD,'default')
    }
}


# S3_CREDENTIALS = [{'s3_bucket': ['xxxxx'],
#                   's3_key': 'xxxxx',
#                   's3_secret': 'xxxxx',
#                   's3_gpg': 'xxxxx'},
#                   {'s3_bucket': ['xxxxx'],
#                   's3_key': 'xxxxx',
#                   's3_secret': 'xxxxx',
#                   's3_gpg': 'xxxxx'}]
#
# FULCRUM_API_KEYS=['xxxx']