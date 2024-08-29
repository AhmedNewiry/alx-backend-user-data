#!/usr/bin/env python3
"""
This module provides utilities for logging and handling personal data.
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates sensitive information in a log message.
    """
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]*',
            f'{field}={redaction}',
            message)
    return message
