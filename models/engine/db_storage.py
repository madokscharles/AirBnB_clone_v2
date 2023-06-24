#!/usr/bin/python3
"""Database storage"""
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv


class DBStorage:
    """ Database storage, creates tables in environment """
    __engine = None
    __session = None

    def __init__(self):
        """ Creates engine """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                    .format(user, passwd, host, db),
                        pool_pre_ping=True))

        if env == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Returns objects_dictionary """
        objects_dictionary = {}
        if cls is None:
            objects_list = self.__session.query(State).all()
            objects_list.extend(self.__session.query(City).all())
            objects_list.extend(self.__session.query(User).all())
            objects_list.extend(self.__session.query(Place).all())
            objects_list.extend(self.__session.query(Review).all())
            objects_list.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects_list = self.__session.query(cls).all()

        for obj in objects_list:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects_dictionary[key] = obj

        return objects_dictionary

    def new(self, obj):
        """Method that adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Method that commits all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Method that deletes from the current database
        session obj if not None"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Method that creates all tables in the database"""

        Base.metadata.create_all(self.__engine)
        my_session = sessionmaker(bind=self.__engine,
                                  expire_on_commit=False)
        Session = scoped_session(my_session)
        self.__session = Session()

    def close(self):
        """Method that closes the session"""
        self.__session.close()
