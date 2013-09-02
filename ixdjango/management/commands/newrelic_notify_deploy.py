"""
Management command to enable New Relic notification of deployments

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

import pwd
import os
from subprocess import Popen, PIPE
from urllib import urlencode

from httplib2 import Http

from django.conf import settings
from django.core.management.base import NoArgsCommand

import newrelic.agent


class Command(NoArgsCommand):
    """
    Loads the fixtures contained inside IX_FIXTURES setting variable.

    See http://redmine.office.infoxchange.net.au/issues/8376
    """

    URL = 'https://rpm.newrelic.com/deployments.xml'

    def handle_noargs(self, **options):
        newrelic.agent.initialize(
            settings.NEW_RELIC_CONFIG,
            settings.NEW_RELIC_ENV
        )

        config = newrelic.agent.global_settings()

        if not config.monitor_mode:
            return

        # get the current git version
        git = Popen(('git', 'describe'), stdout=PIPE)
        ver, _ = git.communicate()
        ver = ver.strip()

        # get the current user
        user = pwd.getpwuid(os.getuid())

        headers = {
            'x-api-key': config.license_key
        }
        post = {
            'deployment[app_name]': config.app_name,
            'deployment[revision]': ver,
            'deployment[user]': '%s (%s)' % (user.pw_gecos, user.pw_name),
        }

        print "Informing New Relic...",

        # post this data
        http = Http()
        response, _ = http.request(self.URL, 'POST',
                                   headers=headers,
                                   body=urlencode(post))

        print response['status']
