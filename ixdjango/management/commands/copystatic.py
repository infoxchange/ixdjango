"""
Copy static files to nginx location

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
import os
from shutil import copy2, copystat

from django.conf import settings
from django.core.management.base import NoArgsCommand


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
            self.stdout.write("Static dir not defined, "
                              "copy static content skipped")
            return

        self.stdout.write("Copying static content to %s" % static_dir)

        self.copytree(settings.STATIC_ROOT, static_dir)

    def copytree(self, src, dst):
        """
        A version of copytree I don't hate
        """

        if not (os.path.exists(dst) and os.path.isdir(dst)):
            self.stdout.write("Creating directory %s" % dst)
            os.makedirs(dst)
            copystat(src, dst)

        for name in os.listdir(src):
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)

            if os.path.isdir(srcname):
                self.stdout.write("Copying directory %s" % name)
                self.copytree(srcname, dstname)
            else:
                self.stdout.write("Copying file %s" % name)
                copy2(srcname, dstname)
