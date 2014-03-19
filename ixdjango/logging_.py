"""
Logging Handler
"""

import logging
import logging.handlers
import socket


class IXAFormatter(logging.Formatter):
    """
    A formatter for IXA logging environment.
    """

    FORMAT = '%(asctime)s {hostname} %(name)s[%(process)d]: %(message)s'.\
        format(
            hostname=socket.gethostname(),
        )
    DATE_FORMAT = '%b %d %H:%M:%S'

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
