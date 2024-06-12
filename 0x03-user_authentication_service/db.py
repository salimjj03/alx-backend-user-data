#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User
from typing import Optional
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str, hashed_password: str) -> Optional[User]:
        """
        two required string arguments: email and hashed_password,
        and returns a User object. The method should save the
        user to the database. No validations are required at
        this stage.
        """

        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **dic: dict) -> User:
        """
        his method takes in arbitrary keyword arguments and
        returns the first row found in the users table as
        filtered by the method’s input arguments. No
        validation of input arguments required at this point.
        """
        keys = ["id", "email", "hashed_password", "session_id", "reset_token"]
        for key in dic.keys():
            if key not in keys:
                raise InvalidRequestError
            result = self._session.query(User).filter_by(**dic).first()
            if result is None:
                raise NoResultFound
            return result

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """
        takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.
        """

        keys = ["id", "email", "hashed_password", "session_id", "reset_token"]
        for key, value in kwargs.items():
            if key not in keys:
                raise ValueError
        user = self.find_user_by(id=user_id)
        setattr(user, key, value)
        self._session.commit()
