"""
Run the application tests, including pre-commit hooks and Lettuce tests.
"""

import sys
from optparse import make_option
from subprocess import check_call, CalledProcessError

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import NoArgsCommand

from iss.tests.migration_dupes import check_migrations


class Command(NoArgsCommand):
    """
    Run the application tests.
    """

    option_list = NoArgsCommand.option_list + (
        make_option('--no-integration',
                    action='store_false',
                    dest='integration',
                    default=True,
                    help="Run integration tests"),
    )

    def handle_noargs(self, **options):
        """
        Run the application tests.
        """

        self.integration = options['integration']

        tests = (
            self.code_style,
            self.migration_dupes,
            self.python_tests,
            self.lettuce_tests,
        )

        failure = False

        for item in tests:
            try:
                item()
            except CalledProcessError:
                failure = True

        if failure:
            sys.exit(1)

    def run_manage(self, *args):
        """
        Run a management command.
        """

        check_call([sys.argv[0]] + [str(arg) for arg in args])

    def code_style(self):
        """
        Check code style.
        """

        check_call(['.githooks/pre-commit', '-f'])

    def migration_dupes(self):
        """
        Check migrations for duplicates
        """
        if not check_migrations('iss'):
            raise ImproperlyConfigured("Duplicate migration IDs")

    def python_tests(self):
        """
        Run Python tests.
        """

        self.run_manage('test', '--noinput')

    def lettuce_tests(self):
        """
        Run Lettuce tests.
        """

        args = ()
        if not self.integration:
            args += ('-t', '-integration')
        self.run_manage('harvest', '-v', 2, *args)
