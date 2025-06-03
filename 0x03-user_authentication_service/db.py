#!/usr/bin/env python3
"""
DB module to manage database operations with SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
from typing import Type


class DB:
    """
    DB class for managing the SQLAlchemy connection and session.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance with SQLite and reset the schema.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database with the given email & hashed password.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds the first user that matches the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first User object matching the filter.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If query parameters are invalid.
        """
        if not kwargs:
            raise InvalidRequestError("No attributes provided")

        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid field: {key}")

        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates attributes of a user with the given user_id.

        Args:
            user_id (int): ID of the user to update.
            **kwargs: Attributes to update.

        Raises:
            ValueError: If any attribute is not part of the User model.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f"Invalid field: {key}")
            setattr(user, key, value)

        self._session.commit()
