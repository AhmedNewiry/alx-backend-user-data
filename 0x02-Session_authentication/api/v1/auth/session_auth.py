#!/usr/bin/env python3
"""
SessionAuth class for session-based authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class that handles session-based authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a user and store it in the 
        user_id_by_session_id dictionary.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            session_id (str): The generated session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        
        Args:
            session_id (str): The session ID.
        
        Returns:
            user_id (str): The corresponding user ID or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
