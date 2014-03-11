"""
Management command to execute several deployment steps with a single command.
More to save flux in the puppet manifest than any effort to reduce typing
required.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
import logging
from shutil import copytree

from django.conf import settings
from django.core.management.base import NoArgsCommand

LOGGER = logging.getLogger(__name__)


class Command(NoArgsCommand):
    """
    Copy static files to nginx location
    """

    def handle_noargs(self, **options):
        try:
            static_dir = settings.NGINX_STATIC_DIR
        except AttributeError:
            static_dir = None

        if not static_dir:
            return

        LOGGER.info("Copying static content to %s", static_dir)

        copytree(settings.STATIC_ROOT, static_dir)
