"""
Management command to execute several deployment steps with a single command.
More to save flux in the puppet manifest than any effort to reduce typing
required.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
import logging
import types

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
            deploy_cmds = None

        # Wrap in a tuple if we were only given one command.
        if isinstance(deploy_cmds, types.StringTypes):
            deploy_cmds = (deploy_cmds,)

        if deploy_cmds:
            for cmd in deploy_cmds:
                # interactive=False is the same as --noinput.
                args = {}
                if type(cmd) is tuple:
                    (cmd, args) = cmd
                management.call_command(cmd, interactive=False, **args)
