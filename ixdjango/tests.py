"""
Configures test suite for the package
"""
from django.utils import unittest

from ixdjango.test_suite.utils import (
    CoreUtilsTests
)


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
