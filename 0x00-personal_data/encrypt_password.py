#!/usr/bin/env python3
"""
This module provides utilities for password encryption.
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """Hash a password with a salt using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
