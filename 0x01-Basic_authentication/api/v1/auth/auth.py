#!/usr/bin/env python3
"""Authentication Management Module"""

from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        Always returns False in this template.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        Always returns None in this template.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Get the current user from the request.
        Always returns None in this template.
        """
        return None
