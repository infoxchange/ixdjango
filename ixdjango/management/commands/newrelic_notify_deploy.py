"""
Management command to enable New Relic notification of deployments

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

import os
from subprocess import call, Popen, PIPE

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
        git = Popen(('git', 'show', ver), stdout=PIPE)
        desc, _ = git.communicate()
        match = re.search('Tagger: (.*) <(.*)>', desc)
        _, username = match.groups()

        ini_file = './conf/newrelic.ini'

        print "Informing New Relic...",

        call(['newrelic-admin',
              'record-deploy',
              ini_file,
              ver,  # description
              ver,  # revision
              '""',  # changelog
              username])
