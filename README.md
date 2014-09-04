=========
IX Django
=========

Management commands for Django application deployments.


Commands provided
-----------------

`deploy`
========

Executes a list of commands declared in `IX_DEPLOY_CMDS` variable in the
application settings file

`loadixfixtures`
================

Loads fixtures declared in `IX_FIXTURES` variable in the application settings
file

`clear_app`
===========

Clear specified app's models of data

`newrelic_notify_deploy`
========================

Uses the settings `NEW_RELIC_CONFIG`, `NEW_RELIC_ENV` and `NEW_RELIC_API_KEY`
to inform New Relic of an application deployment.

Docker Settings
---------------

`ixdjango.docker_settings` provides Django settings module that presets
variables exposed by the Docker environment into your Django application.

Use it as follows:

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Docker container defaults
    # pylint:disable=unused-wildcard-import,import-error,no-name-in-module
    from ixdjango.docker_settings import *
    # pylint:enable=unused-wildcard-import,import-error,no-name-in-module

Provides the following configuration variables:

 * `DEBUG`, `TEMPLATE_DEBUG`, `TASTYPIE_FULL_DEBUG`
 * `DATABASES['default']`
 * `X_FORWARDED_HOST`, `SECURE_PROXY_SSL_HEADER`
 * `MY_SITE_DOMAIN`, `ALLOWED_HOSTS`, `SITE_URL`
 * `EMAIL_HOST`, `EMAIL_PORT`, `DEFAULT_FROM_EMAIL`
 * `LOGGING`
 * `STORAGE_DIR`, `NGINX_STATIC_DIR` (Docker storage locations)
 * `STATIC_ROOT`, `MEDIA_ROOT`


Dependencies
------------

* Django: Depends on Django 1.6, but is being ported to Django 1.7
* Python: 2.7, but Python 3.3 support is being added
* pep8 and pylint: Not required for functionality but we like QC before
committing any code changes so these tools need to be available. Note that
if you'd like to contribute, any code you write must give a clean output with
pep8 and score 10/10 with pylint using the configuration file
conf/pylint.conf in the package
