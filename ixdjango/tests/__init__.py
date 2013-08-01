"""
Hook into the test runner
"""

import subprocess

from django.test.simple import DjangoTestSuiteRunner
from django.utils import unittest

from ixdjango.test_suite.utils import (CoreUtilsTests)


class TestRunner(DjangoTestSuiteRunner):
    """
    Place where we hook into DjangoTestSuiteRunner
    """

    def setup_test_environment(self, *args, **kwargs):
        """
        Hook to set up the test environment
        """

        from django.conf import settings

        print "Running hooks from %s" % __name__

        username = settings.DATABASES['default']['USER']

        print " - Ensure %s can create a test DB" % username
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
