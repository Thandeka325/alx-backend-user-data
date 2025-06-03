#!/usr/bin/env python3
"""
Auth module for handling user registration and authentication.
"""

import bcrypt

from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a randomly-generated salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.

    Returns:
        str: A new UUID string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        Initializes a new Auth instance with a DB connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user if they don't already exist.

        Args:
            email (str): The user's email address.
            password (str): The user's plain-text password.

        Returns:
            User: The created user.

        Raises:
            ValueError: If a user with the email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed.decode('utf-8'))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.
        Args:
            email (str): User's email.
            password (str): User's plain password.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Creates a session ID for the user identified by the given email.

        Args:
            email (str): The user's email.

        Returns:
            Optional[str]: The session ID if the user exists, else None.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session by setting session_id to None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for a user.

        Args:
            email (str): The user's email.
        Returns:
            str: The rest token.
        Raises:
            ValueError: If no user is found with the provided email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")

        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using the provided reset token.
        """
        if not reset_token or not password:
            raise ValueError("Missing token or password")

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed = _hash_password(password).decode('utf-8')
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
