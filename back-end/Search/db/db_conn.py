from sqlalchemy import engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import os


# class for orm connection to the database
class SQLUtil:

    __engine__ = engine
    __session__ = Session
    __connection__ = engine
    __transaction__ = engine

    # creates new engine for orm
    def create_engine(self):
        string = 'mysql+pymysql://root:+uR3s!UPyH7eHb0jUn9Ax5oS]4k@' + os.getenv('DB_HOST') + ':3306/search'
        self.__engine__ = create_engine(string)

    # return current engine for orm
    def get_engine(self):
        return self.__engine__

    # creates new session for orm
    def open_session(self):
        session = sessionmaker()
        session.configure(bind=self.__engine__)
        self.__session__ = session()

    def get_session(self):
        return self.__session__

    def close_session(self):
        self.__session__.close()

    def open_connection(self):
        self.__connection__ = self.get_engine().connect()

    def get_connection(self):
        return self.__connection__

    def close_connection(self):
        return self.__connection__.close()

    def transaction(self):
        self.__transaction__ = self.__connection__.begin()

    def get_transaction(self):
        return self.__transaction__

    def transaction_rollback(self):
        return self.__transaction__.rollback()

    def session_rollback(self):
        return self.__session__.rollback()
