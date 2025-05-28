#!/usr/bin/env python3
"""
SessionExpAuth module for managing session authentication with expiration.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    Session authentication class with expiration logic.
    """

    def __init__(self):
        """Initialize session duration from environment variable"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session with expiration metadata"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID from session ID with expiration check"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict['created_at']
        if (
                created_at + timedelta(seconds=self.session_duration)
                < datetime.now()
        ):
            return None

        return session_dict.get('user_id')
