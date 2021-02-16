from sqlalchemy import engine, Column, String, Enum, DATETIME, ForeignKey, Integer
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
import enum
import os

Base = declarative_base()


class AccountTypeEnum(enum.Enum):
    READER = 0
    EMPLOYEE = 1


class Libraries(Base):
    __tablename__ = 'libraries'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String, nullable=False)
    address = Column('address', String, nullable=False)
    city = Column('city', String, nullable=False)


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    login = Column('login', String, nullable=False)
    password = Column('password', String, nullable=False)
    library_id = Column('library_id', Integer, ForeignKey('libraries.id'), nullable=False)
    address = Column('address', String, nullable=False)
    city = Column('city', String, nullable=False)
    zip_code = Column('zip_code', String, nullable=False)
    date_created = Column('date_created', DATETIME, nullable=False)
    account_type = Column('account_type', Enum(AccountTypeEnum), nullable=False)
    email = Column('email', String, nullable=False)
    library = relationship("Libraries", lazy='subquery')


# class for orm connection to the database
class SQLUtil:
    __engine__ = engine
    __session__ = Session
    __connection__ = engine
    __transaction__ = engine

    # creates new engine for orm
    def create_engine(self):
        string = 'mysql+pymysql://root:6GX3uAqbMoWqx2l-iuDU47YmGkGh@' + os.getenv('DB_HOST') + ':3306/authentication'
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


class DBMethods:

    def __init__(self):
        self.util = SQLUtil()
        self.util.create_engine()
        self.util.open_session()

    def get_all(self, entity):
        try:
            return self.util.get_session().query(entity).all()
        except:
            self.util.session_rollback()
            raise

    def get(self, entity, id):
        try:
            return self.util.get_session().query(entity).get(id)
        except:
            self.util.session_rollback()
            raise

    def get_query(self, entity):
        try:
            return self.util.get_session().query(entity)
        except:
            self.util.session_rollback()
            raise

    def add(self, entity):
        try:
            self.util.get_session().add(entity)
            self.util.get_session().commit()
            return True
        except:
            self.util.session_rollback()
            raise

    def delete_id(self, entity, e_id):
        try:
            a = self.util.get_session().query(entity).get(e_id)
            self.util.get_session().delete(a)
            self.util.get_session().commit()
        except:
            self.util.session_rollback()
            raise

    def update_account(self, e_id, new_entity=Accounts):
        try:
            sel = self.util.get_session().query(Accounts).get(e_id)
            sel.first_name = new_entity.first_name
            sel.last_name = new_entity.last_name
            sel.login = new_entity.login
            sel.password = new_entity.password
            sel.library_id = new_entity.library_id
            sel.address = new_entity.address
            sel.city = new_entity.city
            sel.zip_code = new_entity.zip_code
            sel.date_created = new_entity.date_created
            sel.account_type = new_entity.account_type
            sel.email = new_entity.email
            self.util.get_session().commit()
        except:
            self.util.session_rollback()
            raise
