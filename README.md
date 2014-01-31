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


Dependencies
------------

* Django: Might work on older versions but was developed for 1.3.0.
* pep8 and pylint: Not required for functionality but we like QC before
committing any code changes so these tools need to be available. Note that
if you'd like to contribute, any code you write must give a clean output with
pep8 and score 10/10 with pylint using the configuration file
conf/pylint.conf in the package
