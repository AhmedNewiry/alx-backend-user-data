#!/usr/bin/env python3
"""
Auth module to handle user authentication and registration.
"""
import uuid
from db import DB
from user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _generate_uuid() -> str:
    """
    Generate a new UUID and return it as a string.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid.uuid4())


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
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login by checking the email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the email exists and password
            is correct, False otherwise.
        """
        try:
            # Retrieve the user by email
            user = self._db.find_user_by(email=email)
            # Check if the password matches
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
        self, session_id: Optional[str]
    ) -> Optional[User]:
        """
        Get a user by their session ID.

        Args:
            session_id (str): The session ID of the user.
        Returns:
            User or None: The user corresponding to
            the session ID or None if not found.
        """
        if session_id is None:
            return None

        try:
            # Find user by session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
