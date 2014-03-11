"""
Copy static files to nginx location

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
import logging
import os
from shutil import copy2, copystat

from django.conf import settings
from django.core.management.base import NoArgsCommand

LOGGER = logging.getLogger(__name__)


def copytree(src, dst):
    """
    A version of copytree I don't hate
    """

    if not (os.path.exists(dst) and os.path.isdir(dst)):
        os.makedirs(dst)
        copystat(src, dst)

    for name in os.listdir(src):
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)

        if os.path.isdir(srcname):
            copytree(srcname, dstname)
        else:
            copy2(srcname, dstname)


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
