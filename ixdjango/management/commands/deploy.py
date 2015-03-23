"""
Management command to execute several deployment steps with a single command.
More to save flux in the puppet manifest than any effort to reduce typing
required.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import logging

from django.core.management.base import NoArgsCommand
from django.core import management
from django.conf import settings

LOGGER = logging.getLogger(__name__)


class Command(NoArgsCommand):
    """
    This command is a simple aggregate command to allow us (the devs) to
    easily add deployment steps to our release process e.g. to add a JS minify
    step without needing to add steps to the puppet release manfiest.

    See http://redmine.office.infoxchange.net.au/issues/7854
    """
    def handle_noargs(self, **options):
        try:
            deploy_cmds = settings.IX_DEPLOY_CMDS
        except AttributeError:
            deploy_cmds = []

        # Wrap in a tuple if we were only given one command.
        if isinstance(deploy_cmds, str):
            deploy_cmds = (deploy_cmds,)

        for cmd in deploy_cmds:
            args = []
            kwargs = {}
            if isinstance(cmd, (list, tuple)):
                if len(cmd) == 3:
                    # pylint:disable=unbalanced-tuple-unpacking
                    (cmd, args, kwargs) = cmd
                    # pylint:enable=unbalanced-tuple-unpacking
                else:
                    (cmd, args) = cmd
            # interactive=False is the same as --noinput.
            kwargs.setdefault('interactive', False)
            management.call_command(cmd, *args, **kwargs)
