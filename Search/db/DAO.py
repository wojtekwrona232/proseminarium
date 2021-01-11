from collections import Iterable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, FLOAT
from sqlalchemy.orm import relationship

Base = declarative_base()


class AuthorData(Base):
    __tablename__ = 'authors_data'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)

    @hybrid_property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return str(self.id) + ' ' + self.first_name + ' ' + self.last_name


class TranslatorsData(Base):
    __tablename__ = 'translators_data'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)

    @hybrid_property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return str(self.id) + ' ' + self.first_name + ' ' + self.last_name


class Publishers(Base):
    __tablename__ = 'publishers'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String, nullable=False)

    def __repr__(self):
        return str(self.id) + ' ' + self.name


class Books(Base):
    __tablename__ = 'books'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = Column('isbn', String, nullable=False)
    title = Column('title', String, nullable=False)
    publisher_id = Column('publisher_id', Integer, ForeignKey('publishers.id', ondelete='CASCADE'), nullable=False)
    year_published = Column('year_published', Integer, nullable=False)
    edition_nr = Column('edition_nr', Integer, nullable=False)
    publisher = relationship("Publishers", lazy='subquery')

    def __repr__(self):
        return str(self.id) + ' ' + self.isbn + ' ' + self.title + ' ' + self.publisher.name\
               + ' ' + str(self.year_published) + ' ' + str(self.edition_nr)


class Authors(Base):
    __tablename__ = 'authors'
    book_id = Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    author_id = Column('author_id', Integer, ForeignKey('authors_data.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    book = relationship('Books', lazy='subquery')
    author = relationship('AuthorData', lazy='subquery')

    def __repr__(self):
        return str(self.book.isbn) + ' ' + self.book.title + ' ' + str(self.book.year_published)\
               + ' ' + self.author.first_name + ' ' + self.author.last_name


class Translators(Base):
    __tablename__ = 'translators'
    book_id = Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    translator_id = Column('translator_id', Integer, ForeignKey('translators_data.id', ondelete='CASCADE'),  primary_key=True, nullable=False)
    book = relationship('Books', lazy='subquery')
    translator = relationship('TranslatorsData', lazy='subquery')

    def __repr__(self):
        return str(self.book.isbn) + ' ' + self.book.title + ' ' + str(self.book.year_published)\
               + ' ' + self.translator.first_name + ' ' + self.translator.last_name
