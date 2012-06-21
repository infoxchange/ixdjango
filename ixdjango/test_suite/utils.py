"""
Tests for WSX Core Utility Classes/functions
"""
#
# pylint:disable=R0904
# - R0904: Stuff inheriting from TestCase always has too many public methods
#
from django.test import TestCase
from django.http import HttpRequest, QueryDict

from ixdjango.utils import (
    random_string,
    querydict_to_dict,
    remote_addr_from_request,
    flatten_request_headers,
    flat_header_val_to_dict)


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

    def test_flatten_request_headers(self):
        """
        Convert a dict to a valid string
        """
        headers_in = {
            'Authorization': {
                'oauth_consumer_key': 'qwertyuiop',
                'oauth_nonce': 'asdfghjkl'
            },
            'content-type': 'text/html'
        }
        expected = {
            'Authorization': \
                'oauth_consumer_key="qwertyuiop",oauth_nonce="asdfghjkl"',
            'content-type': 'text/html'}
        self.assertEqual(flatten_request_headers(headers_in), expected)

    def test_flat_header_val_to_dict(self):
        """
        Turn paramaters contained in a header to a dict
        """
        header_val = 'a="b" ,c="d" ,e="f", g= "h" '
        expected = {'a': 'b', 'c': 'd', 'e': 'f', 'g': 'h'}
        self.assertEqual(flat_header_val_to_dict(header_val), expected)
