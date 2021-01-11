import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

TranslatorsApi = Blueprint('translators', __name__)


def make_json(obj):
    return {
        "book_id": obj.book_id,
        "author_id": obj.author_id
    }


@TranslatorsApi.route('/all', methods=['POST'])
def get_translators_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(Translators)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@TranslatorsApi.route('/book-isbn', methods=['POST'])
def get_translators_by_book():
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

    query = DBMethods().get_query(Translators).filter(Translators.book_id.contains(book_id_))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@TranslatorsApi.route('/translator-id', methods=['POST'])
def get_translators_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_translator = DBMethods().get_query(TranslatorsData).filter(
        TranslatorsData.first_name.contains(obj['translator']['first_name']),
        TranslatorsData.last_name.contains(obj['translator']['last_name']))

    new_translator_id = 0
    for m in new_translator:
        new_translator_id = m.id

    query = DBMethods().get_query(Translators).filter(Translators.translator_id.contains(new_translator_id))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@TranslatorsApi.route('/delete', methods=['POST'])
def delete_translators():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Translators).filter(Translators.book_id.contains(obj['book_id']),
                                                      Translators.translator_id.contains(obj['translator_id']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(Translators, m.id)
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@TranslatorsApi.route('/update', methods=['POST'])
def update_translators():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new = [obj['new']['book_id'], obj['new']['author_id']]
    query = DBMethods().get_query(Translators).filter(Translators.book_id.contains(obj['old']['book_id']),
                                                      Translators.translator_id.contains(obj['old']['translator_id']))
    for m in query:
        DBMethods().update_books_author(m.book_id, m.author_id, new)
    l = []
    query = DBMethods().get_query(Translators).filter(Translators.book_id.contains(obj['new']['book_id']),
                                                      Translators.translator_id.contains(obj['new']['translator_id']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@TranslatorsApi.route('/add-new', methods=['POST'])
def add_new_translators():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_book = DBMethods().get_query(Books).filter(Books.isbn.contains(obj['isbn']))
    new_book_id = 0
    for m in new_book:
        new_book_id = m.id

    new_translator = DBMethods().get_query(TranslatorsData).filter(
        TranslatorsData.first_name.contains(obj['translator']['first_name']),
        TranslatorsData.last_name.contains(obj['translator']['last_name']))

    new_translator_id = 0
    for m in new_translator:
        new_translator_id = m.id

    d = Translators(book_id=new_book_id, translator_id=new_translator_id)

    DBMethods().add_entity(d)

    query = DBMethods().get_query(Translators).filter(Translators.book_id.contains(new_book_id),
                                                      Translators.translator_id.contains(new_translator_id))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "Translators": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

