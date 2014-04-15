"""
Management command to enable New Relic notification of deployments

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

import os
from subprocess import call, Popen, PIPE

from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    """
    Notify New Relic of the new version
    """

    def handle_noargs(self, **options):
        # get the current git version
        git = Popen(('git', 'describe'), stdout=PIPE)
        ver, _ = git.communicate()
        ver = ver.strip()

        # The the tagger name and email
        git = Popen(('git', 'log', ver, '--format=%ae', '-1'), stdout=PIPE)
        username, _ = git.communicate()
        username = username.strip()

        ini_file = os.environ.get('NEW_RELIC_CONFIG_FILE',
                                  settings.NEW_RELIC_CONFIG)

        print "Informing New Relic...",

        call(['newrelic-admin',
              'record-deploy',
              ini_file,
              ver,  # description
              ver,  # revision
              '',  # changelog
              username])
