"""
Hook into the test runner
"""

from __future__ import print_function

import subprocess

# pylint:disable=import-error,no-name-in-module
try:
    from django.test.runner import DiscoverRunner as BaseTestRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as BaseTestRunner
from django.utils import unittest
# pylint:enable=import-error,no-name-in-module

from ixdjango.test_suite.utils import (CoreUtilsTests)


class TestRunner(BaseTestRunner):
    """
    Place where we hook into DjangoTestSuiteRunner
    """

    def setup_test_environment(self, *args, **kwargs):
        """
        Hook to set up the test environment
        """

        from django.conf import settings

        print("Running hooks from %s" % __name__)

        username = settings.DATABASES['default']['USER']

        print(" - Ensure %s can create a test DB" % username)
        subprocess.call(['sudo', 'su', 'postgres', '-c',
                         "psql -c 'alter user %s with createdb;'" % username])

        return super(TestRunner, self).setup_test_environment(*args, **kwargs)


def suite():
    """
    Put together a suite of tests to run for the application
    """
    loader = unittest.TestLoader()

    all_tests = unittest.TestSuite([
        #
        # Utilities test cases
        #
        loader.loadTestsFromTestCase(CoreUtilsTests)
    ])

    return all_tests
