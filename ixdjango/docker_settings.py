"""
Standard config for loading Django settings from Docker
"""

import logging
import logging.handlers
import os
import socket
import sys

import dj_database_url

# this dark incantation copies the settings set so far in the main config
# into our address space
locals().update(vars(sys.modules[os.environ['DJANGO_SETTINGS_MODULE']]))

assert BASE_DIR, "BASE_DIR must be defined"

# Environment
ENVIRONMENT = os.environ.get('ENVIRONMENT', None)

# Debugging
DEBUG = ENVIRONMENT in ('dev_local', 'dev', 'test')
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

# Databases
if ENVIRONMENT:
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DB_DEFAULT_URL'])
    }
else:
    DATABASES = {}

# Trust nginx
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Site domain and URL
MY_SITE_DOMAIN = os.environ.get('SITE_DOMAIN')
if MY_SITE_DOMAIN:
    ALLOWED_HOSTS = (MY_SITE_DOMAIN,)

SITE_URL = '{0}://{1}'.format(os.environ.get('SITE_PROTOCOL'), MY_SITE_DOMAIN)

# Email
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
DEFAULT_FROM_EMAIL = 'do.not.reply@%s' % MY_SITE_DOMAIN

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
            'level': 'INFO',
            'handlers': [],
            'propagate': True,
        },
        'django.request': {
            'level': 'INFO',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'django.db': {
            'level': 'WARNING',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'django.security': {
            'level': 'INFO',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'requests': {
            'level': 'WARNING',
            'handlers': [],
            'propagate': True,
        }
    },
}

if ENVIRONMENT not in (None, 'dev_local',):
    # configure Kibana on sites other than dev_local
    # N.B. Travis is also running as dev_local

    LOGGING_ADDRESS = (os.environ.get('SYSLOG_SERVER', 'localhost'),
                       int(os.environ.get('SYSLOG_PORT',
                                          logging.handlers.SYSLOG_UDP_PORT)))
    LOGGING_SOCKTYPE = ({
        'tcp': socket.SOCK_STREAM,
        'udp': socket.SOCK_DGRAM,
    })[os.environ.get('SYSLOG_PROTO', 'udp')]

    LOGGING['handlers']['kibana'] = {
        'level': 'INFO',
        'class': 'ixdjango.logging_.SysLogHandler',
        'address': LOGGING_ADDRESS,
        'socktype': LOGGING_SOCKTYPE,
        'formatter': 'ixa',
    }

    # send all logs to Kibana
    for logger in LOGGING['loggers'].values():
        logger['handlers'].insert(0, 'kibana')
else:
    # show request logs on the console
    for logger in LOGGING['loggers'].values():
        logger['handlers'].insert(0, 'console')


# File locations
if ENVIRONMENT == 'dev_local':
    STORAGE_DIR = BASE_DIR
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

else:
    STORAGE_DIR = '/storage'
    STATIC_ROOT = '/static'

MEDIA_ROOT = os.path.join(STORAGE_DIR, 'media')
