"""
Standard config for loading Django settings from Docker
"""
from __future__ import absolute_import, unicode_literals

import logging
import logging.handlers
import os
import socket
import sys
import warnings

# Copy BASE_DIR from the main configuration
BASE_DIR = getattr(
    sys.modules[os.environ['DJANGO_SETTINGS_MODULE']], 'BASE_DIR', None)

assert BASE_DIR, "BASE_DIR setting must be defined."

# Environment
ENVIRONMENT = os.environ.get('ENVIRONMENT', None)
if ENVIRONMENT == 'dev_local':
    DEVNAME = os.environ['DEVNAME']

# Debugging
DEBUG = ENVIRONMENT in ('dev_local', 'dev', 'test')
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

# Trust nginx
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allowed hosts, Site domain and URL
ALLOWED_HOSTS = os.environ.get('SITE_DOMAIN', '').split('|')
MY_SITE_DOMAIN = ALLOWED_HOSTS[0]
SITE_URL = '{0}://{1}'.format(os.environ.get('SITE_PROTOCOL', ''),
                              MY_SITE_DOMAIN)

# Databases
DATABASES = {}

if 'DB_DEFAULT_URL' in os.environ:
    import dj_database_url  # pylint:disable=wrong-import-position

    if ENVIRONMENT:
        DATABASES = {
            'default': dj_database_url.parse(os.environ['DB_DEFAULT_URL'])
        }

# Elasticsearch
ELASTICSEARCH_INDEX_NAME = os.environ.get('ELASTICSEARCH_INDEX_NAME')
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URLS', '').split('|')

# Memcache
try:
    # pylint:disable=unused-import,import-error,wrong-import-position
    import memcache
    # pylint:enable=unused-import,import-error,wrong-import-position

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.environ['MEMCACHE_HOSTS'].split('|'),
            'KEY_PREFIX': os.environ['MEMCACHE_PREFIX'],
        },
    }

except (ImportError, KeyError):
    pass

# Email
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
DEFAULT_FROM_EMAIL = 'do.not.reply@%s' % MY_SITE_DOMAIN

# Secret key
if not hasattr(
        sys.modules[os.environ['DJANGO_SETTINGS_MODULE']],
        'SECRET_KEY'
):
    warnings.warn((
        "Please define SECRET_KEY before importing {0}, as a fallback "
        "for when the environment variable is not available."
    ).format(__name__))
try:
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.pop('SECRET_KEY')
except KeyError:
    pass

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'ixa': {
            '()': 'ixdjango.logging_.IXAFormatter',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'gunicorn': {
            'level': 'DEBUG' if ENVIRONMENT == 'dev_local' else 'INFO',
            'handlers': [],
            'propagate': True,
        },
        'django.request': {
            'level': 'INFO',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'django.db': {
            'level': 'INFO' if ENVIRONMENT == 'dev_local' else 'WARNING',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'django.security': {
            'level': 'INFO',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'requests': {
            'level': 'INFO' if ENVIRONMENT == 'dev_local' else 'WARNING',
            'handlers': [],
            'propagate': True,
        },
        'newrelic': {
            'level': 'INFO',
            'handlers': [],
            'propagate': True,
        },
    },
}

if ENVIRONMENT not in (None, 'dev_local',):
    # configure logstash on sites other than dev_local
    # N.B. Travis is also running as dev_local

    LOGGING_ADDRESS = (os.environ.get('SYSLOG_SERVER', 'localhost'),
                       int(os.environ.get('SYSLOG_PORT',
                                          logging.handlers.SYSLOG_UDP_PORT)))
    LOGGING_SOCKTYPE = ({
        'tcp': socket.SOCK_STREAM,
        'udp': socket.SOCK_DGRAM,
    })[os.environ.get('SYSLOG_PROTO', 'udp')]

    LOGGING['handlers']['logstash'] = {
        'level': 'DEBUG' if DEBUG else 'INFO',
        'class': 'ixdjango.logging_.SysLogHandler',
        'address': LOGGING_ADDRESS,
        'socktype': LOGGING_SOCKTYPE,
        'formatter': 'ixa',
    }

    # send all logs to logstash
    for logger in LOGGING['loggers'].values():
        logger['handlers'].insert(0, 'logstash')

    CONSOLE_OUTPUT_DISABLED = True  # Default; may be overridden

else:
    CONSOLE_OUTPUT_DISABLED = False  # Default; may be overridden

CONSOLE_OUTPUT_DISABLED = bool(os.environ.get('CONSOLE_OUTPUT_DISABLED',
                                              CONSOLE_OUTPUT_DISABLED))

if not CONSOLE_OUTPUT_DISABLED:
    # show request logs on the console
    for logger in LOGGING['loggers'].values():
        logger['handlers'].insert(0, 'console')


# File locations
if ENVIRONMENT == 'dev_local':
    STORAGE_DIR = BASE_DIR
    NGINX_STATIC_DIR = None

else:
    STORAGE_DIR = '/storage'
    NGINX_STATIC_DIR = '/static'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(STORAGE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
