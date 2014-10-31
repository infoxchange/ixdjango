"""
Logging Handler
"""

import logging
import logging.handlers
import os
import re
import socket
import time


class IXAFormatter(logging.Formatter):
    """
    A formatter for IXA logging environment.
    """

    HOSTNAME = re.sub(
        r':\d+$', '', os.environ.get('SITE_DOMAIN', socket.gethostname()))
    FORMAT = '%(asctime)s {hostname} %(name)s[%(process)d]: %(message)s'.\
        format(hostname=HOSTNAME)
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    converter = time.gmtime

    def __init__(self):
        super(IXAFormatter, self).__init__(fmt=self.FORMAT,
                                           datefmt=self.DATE_FORMAT)

    def format(self, record):
        # strip newlines
        message = super(IXAFormatter, self).format(record)
        message = message.replace('\n', ' ')
        message += '\n'
        return message


class SysLogHandler(logging.handlers.SysLogHandler):
    """
    A SysLogHandler not appending NUL character to messages
    """
    append_nul = False
