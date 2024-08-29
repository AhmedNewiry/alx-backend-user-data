#!/usr/bin/env python3
"""
This module provides utilities for logging and handling personal data.
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates sensitive information in a log message.
    """
    return re.sub(
        r'(?<=({})=)[^{}]+'.format('|'.join(fields), separator),
        redaction,
        message
    )
