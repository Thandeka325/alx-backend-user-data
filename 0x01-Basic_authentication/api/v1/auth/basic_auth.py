#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Tuple


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64-encoded authorization header to a UTF-8 string

        Args:
            base64_authorization_header (str): Base64 string

        Returns:
            str: Decoded UTF-8 string or None if invalid
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            import base64
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from a Base64 decoded
        authorization header

        Args:
            decoded_base64_authorization_header (str): Decoded Base64 str

        Returns:
            tuple: (email, password) if valid, otherwise (None, None)
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password

        Args:
            user_email (str): The user's email
            user_pwd (str): The user's password

        Returns:
            User: The user instance if found and valid, otherwise None
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
