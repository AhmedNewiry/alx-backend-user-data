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
    Hash the given password using bcrypt and
    return the hashed password as bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize Auth with a DB instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to register
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
