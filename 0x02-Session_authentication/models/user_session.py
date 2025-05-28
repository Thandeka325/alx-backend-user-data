#!/usr/bin/env python3
"""
UserSession model for handling DB-stored sessions
"""
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """
    Class for storing user sessions in database/file storage
    Attributes:
        user_id: string - the ID of the user
        session_id: string - the ID of the session
        created_at: datetime - when the session was created
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = kwargs.get('created_at') or datetime.now()
