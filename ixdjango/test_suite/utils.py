"""
Tests for WSX Core Utility Classes/functions
"""
#
# pylint:disable=invalid-name,too-many-public-methods
# - Classes inheriting from TestCase always has too many public methods
# - Test function names too long; following a pattern
#
from django.test import TestCase
from django.http import HttpRequest, QueryDict

from ixdjango.utils import (
    random_string,
    querydict_to_dict,
    remote_addr_from_request,
    flatten_request_header,
    flat_header_val_to_dict,
    flatten_auth_header,
    flat_auth_header_val_to_data)


class CoreUtilsTests(TestCase):
    """
    Test cases for utils functions
    """
    def test_random_string(self):
        """
        just make sure we get the right lengths
        """
        self.assertEqual(len(random_string()), 10)
        self.assertEqual(len(random_string(length=5)), 5)

    def test_querydict_to_dict(self):
        """
        especially make sure items that do not have array of values are
        not converted to arrays (func uses get_list() for consistency)
        """
        qdict = QueryDict("a=b&b=c&b=d&c=e&c=&f=&g=&g=")
        self.assertEqual(
            querydict_to_dict(qdict),
            {'a': 'b',
             'b': ['c', 'd'],
             'c': ['e', ''],
             'f': '',
             'g': ['', '']}
        )

    def test_remote_addr_from_request(self):
        """
        proxied requests must be handled correctly
        """
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '192.168.1.1'
        self.assertEqual(remote_addr_from_request(req), '192.168.1.1')
        req.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.2'
        self.assertEqual(remote_addr_from_request(req), '192.168.1.2')

    def test_flatten_request_header(self):
        """
        Convert a dict to a valid string
        """
        header = {'oauth_consumer_key': 'qwertyuiop',
                  'oauth_nonce': 'asdfghjkl'}

        expected = 'oauth_consumer_key="qwertyuiop",oauth_nonce="asdfghjkl"'

        self.assertEqual(flatten_request_header(header), expected)

    def test_flat_header_val_to_dict(self):
        """
        Turn paramaters contained in a header to a dict
        """
        header_val = 'a="b" ,c="d" ,e="f", g= "h" '
        expected = {'a': 'b', 'c': 'd', 'e': 'f', 'g': 'h'}
        self.assertEqual(flat_header_val_to_dict(header_val), expected)

        header_val = 'notadict'
        self.assertEqual(flat_header_val_to_dict('notadict'), {})

    def test_flatten_auth_header(self):
        """
        Auth headers contain a auth type at the start
        """
        header = {'oauth_consumer_key': 'qwertyuiop',
                  'oauth_nonce': 'asdfghjkl'}
        expected = \
            'OAuth oauth_consumer_key="qwertyuiop",oauth_nonce="asdfghjkl"'
        self.assertEqual(flatten_auth_header(header, 'OAuth'), expected)

    def test_flat_auth_header_val_to_data(self):
        """
        Should pass header params and type separately, data should extract
        even if auth type is not there
        """
        without_at = 'oauth_consumer_key="qwertyuiop",oauth_nonce="asdfghjkl"'
        with_at = 'OAuth %s' % without_at

        expected_data = {'oauth_consumer_key': 'qwertyuiop',
                         'oauth_nonce': 'asdfghjkl'}

        self.assertEqual(flat_auth_header_val_to_data(without_at),
                         (expected_data, None))
        self.assertEqual(flat_auth_header_val_to_data(with_at),
                         (expected_data, 'OAuth'))
