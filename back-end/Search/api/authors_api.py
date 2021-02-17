import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

authorsAPI = Blueprint('authors', __name__)


def make_json(obj):
    return {
        "book_id": obj.book_id,
        "author_id": obj.author_id
    }


@authorsAPI.route('/all', methods=['POST'])
def get_authors_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(Authors)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsAPI.route('/book-isbn', methods=['POST'])
def get_authors_by_book_isbn():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    book_id = DBMethods().get_query(Books).filter(Books.isbn.contains(obj['isbn']))

    book_id_ = 0
    for m in book_id:
        book_id_ = m.id

    query = DBMethods().get_query(Authors).filter(Authors.book_id.contains(book_id_))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsAPI.route('/author-id', methods=['POST'])
def get_authors_by_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Authors).filter(Authors.author_id.contains(obj['author_id']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsAPI.route('/delete', methods=['POST'])
def delete_authors():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Authors).filter(Authors.book_id.contains(obj['book_id']),
                                                  Authors.author_id.contains(obj['author_id']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(Authors, m.id)
    file = {
        "meta": meta,
        "authors": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsAPI.route('/update', methods=['POST'])
def update_authors():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new = [obj['new']['book_id'], obj['new']['author_id']]
    query = DBMethods().get_query(Authors).filter(Authors.book_id.contains(obj['old']['book_id']),
                                                  Authors.author_id.contains(obj['old']['author_id']))
    for m in query:
        DBMethods().update_books_author(m.book_id, m.author_id, new)
    l = []
    query = DBMethods().get_query(Authors).filter(Authors.book_id.contains(obj['new']['book_id']),
                                                  Authors.author_id.contains(obj['new']['author_id']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsAPI.route('/add-new', methods=['POST'])
def add_new_authors():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_book = DBMethods().get_query(Books).filter_by(id=obj['id']).first()

    new_author = DBMethods().get_query(AuthorData).filter_by(id=obj['author_id']).first()

    d = Authors(book_id=new_book.id, author_id=new_author.id)

    DBMethods().add_entity(d)

    query = DBMethods().get_query(Authors).filter_by(book_id=new_book.id, author_id=new_author.id).first()

    file = {
        "meta": meta,
        "authors": make_json(query)
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

