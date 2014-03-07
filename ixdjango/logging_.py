"""
Logging Handler
"""

import logging
import logging.handlers
import socket
from copy import copy


class IXAFormatter(logging.Formatter):

    FORMAT = '%(asctime)s {hostname} %(name)s[%(process)d]: %(message)s'.format(
        hostname=socket.gethostname(),
    )
    DATE_FORMAT = '%b %d %H:%M:%S'

    def __init__(self):
        super(IXAFormatter, self).__init__(fmt=self.FORMAT,
                                           datefmt=self.DATE_FORMAT)

    def format(self, record):
        record = copy(record)

        # strip newlines
        record.message = record.message.replace('\n', ' ')

        return super(IXAFormatter, self).format(record)


class SysLogHandler(logging.handlers.SysLogHandler):
    """
    A SysLogHandler not appending NUL character to messages
    """
    append_nul = False
