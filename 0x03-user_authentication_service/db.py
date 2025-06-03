#!/usr/bin/env python3
"""
DB module to manage database operations with SQLAlchemy.
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    DB class for managing SQLAlchemy connection and session.
    """

    def __init__(self) -> None:
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        Add a new user and return the User instance.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except Exception:
            self._session.rollback()
            return None

    def find_user_by(self, **kwargs) -> User:
        """
        Finds the first user that matches the given fields.
        """
        if not kwargs:
            raise InvalidRequestError()

        fields = []
        values = []

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
            fields.append(getattr(User, key))
            values.append(value)

        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()

        if result is None:
            raise NoResultFound()

        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user’s fields with given values.
        """
        self.find_user_by(id=user_id)

        update_data = {}
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            update_data[getattr(User, key)] = value

        self._session.query(User).filter_by(id=user_id).update(
            update_data, synchronize_session=False
        )
        self._session.commit()
