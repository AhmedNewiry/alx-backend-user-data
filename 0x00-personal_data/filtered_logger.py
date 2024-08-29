#!/usr/bin/env python3
"""
This module provides utilities for
logging and handling personal data.
It includes functions to obfuscate sensitive
information in log messages.
"""

import re
import logging


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates sensitive information in a log message.
    """
    pattern = r'({}=)[^{}}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: m.group(1) + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialize the formatter with fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with redacted sensitive information."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
