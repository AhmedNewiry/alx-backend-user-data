#!/usr/bin/env python3
"""
This module provides utilities for logging and handling personal data.
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates sensitive information in a log message.
    """
    pattern = r'(?<=({})=)[^{}]+'.format('|'.join(fields), separator)
    return re.sub(pattern, redaction, message)
