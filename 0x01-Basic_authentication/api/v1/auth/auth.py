#!/usr/bin/env python3
"""
This module defines the base class for handling API authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path

        Args:
            path (str): The request path
            excluded_paths (List[str]): A list of paths that
            do not require authentication

        Returns:
            bool: False by default
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path == path:
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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request

        Args:
            request (flask.Request): The request object

        Returns:
            TypeVar('User'): None by default
        """
        return None
