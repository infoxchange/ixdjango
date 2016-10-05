"""
Management command to load data from the fixtures contained inside IX_FIXTURES.
Allows different data to be loaded depending on whether we are in production,
staging, etc.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""
from __future__ import print_function

import logging

import six
from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Loads the fixtures contained inside IX_FIXTURES setting variable.

    See http://redmine.office.infoxchange.net.au/issues/8376
    """

    def handle(self, *args, **options):
        """
        Load the fixtures.
        """
        try:
            ix_fixtures = settings.IX_FIXTURES
        except AttributeError:
            ix_fixtures = None

        # Wrap in an tuple if we were only given one command.
        if isinstance(ix_fixtures, six.string_types):
            ix_fixtures = (ix_fixtures,)

        if ix_fixtures:
            print("Loading IX_FIXTURES: {0}".format(','.join(ix_fixtures)))
            management.call_command(
                "loaddata",
                *ix_fixtures,
                interactive=False
            )
        else:
            print("loadixfixtures does nothing unless settings.IX_FIXTURES "
                  "has been configured. Could it be that this application "
                  "does not use loadixfixtures?\n\n"
                  "Have you tried `./manage.py loaddata` instead?")
