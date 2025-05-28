#!/usr/bin/env python3
"""
This module defines the base class for handling API authentication.
"""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """
    Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path

        Returns True if the path is not in excluded_paths
        Supports wildcard * at the end of excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if not excluded_path.endswith('/'):
                    excluded_path += '/'
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request

        Args:
            request (flask.Request): The request object

        Returns:
            str: None by default
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request

        Args:
            request (flask.Request): The request object

        Returns:
            TypeVar('User'): None by default
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the session cookie value from the request

        Args:
            request (flask.Request): The request obect
        Returns:
            str: The value of the session cookie or None
        """
        if request is None:
            return None

        session_name = getenv("SESSION_NAME")
        if session_name is None:
            return None

        return request.cookies.get(session_name)
