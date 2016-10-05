"""
Management command to enable New Relic notification of deployments

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

from __future__ import print_function

import os
from subprocess import call, Popen, PIPE

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Notify New Relic of the new version
    """

    def handle(self, *args, **options):
        """
        Call the newrelic-admin command with the new version.
        """
        # get the current git version
        git = Popen(('git', 'describe'), stdout=PIPE)
        ver, _ = git.communicate()
        ver = ver.strip()

        # The the tagger name and email
        git = Popen(('git', 'log', ver, '--format=%ae', '-1'), stdout=PIPE)
        username, _ = git.communicate()
        username = username.strip()

        try:
            ini_file = os.environ['NEW_RELIC_CONFIG_FILE']
        except KeyError:
            ini_file = settings.NEW_RELIC_CONFIG

        print("Informing New Relic...", end=' ')

        call(['newrelic-admin',
              'record-deploy',
              ini_file,
              ver,  # description
              ver,  # revision
              '',  # changelog
              username])
