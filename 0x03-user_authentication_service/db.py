#!/usr/bin/env python3
"""DB module
"""
from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar("User"):
        """ adds a user to the database """
        if email is None or hashed_password is None:
            return None
        user = User(email, hashed_password)
        # user.email = email
        # user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> TypeVar("User"):
        """ Finds a user based on given keyword args """
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: str, **kwargs):
        """ updates a users data """
        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if not hasattr(User, k):
                    raise ValueError
                setattr(user, k, v)
            self._session.commit()
            return None
        except NoResultFound:
            return None
