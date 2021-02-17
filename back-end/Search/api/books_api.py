import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

BooksAPI = Blueprint('books', __name__)


def make_json(obj):
    return {
        "id": obj.id,
        "isbn": obj.isbn,
        "title": obj.title,
        "publisher_id": obj.publisher_id,
        "year_published": obj.year_published,
        "edition_nr": obj.edition_nr
    }


@BooksAPI.route('/all', methods=['POST'])
def get_books_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(Books)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Books": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/id', methods=['POST'])
def get_books_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Books).filter_by(id=obj['id']).first()
    file = {
        "meta": meta,
        "Books": make_json(query)
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/title', methods=['POST'])
def get_books_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Books).filter(Books.title.contains(obj['title']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Books": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/publisher', methods=['POST'])
def get_books_publisher():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_publisher = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['publisher_name']))
    new_publisher_id = 0
    for m in new_publisher:
        new_publisher_id = m.id

    query = DBMethods().get_query(Books).filter(Books.publisher_id.contains(new_publisher_id))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Books": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/delete', methods=['POST'])
def delete_books_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Books).filter(Books.isbn.contains(obj['isbn']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(Books, m.id)
    file = {
        "meta": meta,
        "Books": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/update', methods=['POST'])
def update_book():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_data = [obj['isbn'], obj['title'], obj['publisher_id'], obj['year_published'], obj['edition_nr']]
    query = DBMethods().get_query(Books).filter(Books.isbn.contains(obj['old']['isbn']))
    for m in query:
        DBMethods().update_books(m.id, new_data)
    l = []
    query = DBMethods().get_query(Books).filter(Books.isbn.contains(obj['new']['isbn']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Books": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@BooksAPI.route('/add-new', methods=['POST'])
def add_new_book():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_publisher = DBMethods().get_query(Publishers).filter_by(id=obj['publisher_id']).first()

    d = Books(isbn=obj['isbn'],
              title=obj['title'],
              publisher_id=obj['publisher_id'],
              year_published=obj['year_published'],
              edition_nr=obj['edition_nr'])

    DBMethods().add_entity(d)

    query = DBMethods().get_query(Books).filter_by(isbn=obj['isbn']).first()
    file = {
        "meta": meta,
        "Books": make_json(query)
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

