"""
Utility classes/functions
"""
from random import choice
import re


class RequestHeaderException(Exception):
    """
    Custom exception to deal with request header errors
    """
    def __str__(self):
        """
        Add info specific to this exception
        """
        return (
            "Bad Request Header: %s"
            % super(RequestHeaderException, self).__str__()
        )


def random_string(
    length=10,
    chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
):
    """
    Generates a random string of length specified and using supplied chars.
    Useful for salting hashing functions
    """
    #
    # pylint:disable=W0612
    # Not using i but it has to be there
    #
    return ''.join([choice(chars) for i in range(length)])


def querydict_to_dict(querydict):
    """
    Converts a QueryDict instance (i.e.request params) into a plain
    dictionary
    """
    pure_dict = {}
    for item_key in querydict.keys():
        item_val_list = querydict.getlist(item_key)
        if item_val_list:
            if len(item_val_list) == 0:
                pure_dict[item_key] = None
            if len(item_val_list) == 1:
                pure_dict[item_key] = item_val_list[0]
            else:
                pure_dict[item_key] = item_val_list
        else:
            pure_dict[item_key] = None
    return pure_dict


def remote_addr_from_request(request):
    """
    Returns the correct remote address from the request object. If the
    request was proxied, this correct information is in HTTP_X_FORWARDED_FOR
    """
    if not request:
        raise TypeError("No request passed to function")
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def flatten_request_header(header):
    """
    Transform a dict representing header parameters into a flat string of
    comma separated parameters suitable for inserting into the actual
    headers
    """
    flattened_header = ''
    if isinstance(header, dict):
        contents = []
        for content_key, content_val in header.items():
            contents.append('%s="%s"' % (content_key, content_val))

        flattened_header = ','.join(contents)
    else:
        flattened_header = str(header)

    return flattened_header


def flatten_auth_header(headers_dict, auth_type):
    """
    Auth headers have auth type at the start of the string
    """
    return "%s %s" % (auth_type, flatten_request_header(headers_dict))


def flat_header_val_to_dict(header_val):
    """
    Transform a header string of comma separated parameters into a dict
    """
    val_dict = {}
    val_comps = header_val.rsplit(',')
    if len(val_comps):
        for val_comp in val_comps:
            key, sep, val = val_comp.partition("=")
            if sep != "=":
                raise RequestHeaderException("non key/val entry in header")
            key = key.strip()
            val = val.strip()
            val = val.strip('"')
            if key in val_dict:
                if isinstance(val_dict[key], list):
                    val_dict[key].append(val)
                else:
                    val_dict[key] = [val_dict[key], val]
            else:
                val_dict[key] = val
    return val_dict


def flat_auth_header_val_to_data(header_val):
    """
    Capture auth type from the string and then remove it before passing on to
    flat_header_val_to_dict
    """
    match = re.match(r'^([\S]+[\s]+)?(.*)$', header_val)
    if match and match.group(1):
        return (flat_header_val_to_dict(match.group(2).strip()),
                match.group(1).strip())

    return (flat_header_val_to_dict(header_val), None)