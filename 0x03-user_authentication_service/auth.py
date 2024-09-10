#!/usr/bin/env python3
"""
Auth module to handle user authentication and registration.
"""

from db import DB
from user import User
from sqlalchemy.exc import IntegrityError
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hash the given password using bcrypt and return the hashed password as bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
