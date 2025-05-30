#!/usr/bin/env python3
"""
Session-based authentication with DB persistence
"""
from datetime import datetime
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication with persistent storage"""

    def create_session(self, user_id=None):
        """Creates and stores session in DB"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves a user ID by session_id from the DB"""
        if session_id is None:
            return None

        user_sessions = storage.all(UserSession).values()
        for session in user_sessions:
            if session.session_id == session_id:
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """Deletes the session from storage"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = storage.all(UserSession).values()
        for session in user_sessions:
            if session.session_id == session_id:
                storage.delete(session)
                storage.save()
                return True
        return False
