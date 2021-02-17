import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

authorsDataAPI = Blueprint('authors-data', __name__)


def make_json(obj):
    return {
        "id": obj.id,
        "first_name": obj.first_name,
        "last_name": obj.last_name
    }


@authorsDataAPI.route('/all', methods=['POST'])
def get_authors_data_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(AuthorData)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/id', methods=['POST'])
def get_authors_data_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        },
        "title": "buyers with specified id"
    }
    query = DBMethods().get_query(AuthorData).filter_by(id=obj['id']).first()
    file = {
        "meta": meta,
        "authors_data": make_json(query)
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/first-name', methods=['POST'])
def get_authors_data_first_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(AuthorData).filter(AuthorData.first_name.contains(obj['first_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/last-name', methods=['POST'])
def get_authors_data_last_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(AuthorData).filter(AuthorData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/delete', methods=['POST'])
def delete_authors_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(AuthorData).filter(AuthorData.first_name.contains(obj['first_name']),
                                                     AuthorData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(AuthorData, m.id)
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/update', methods=['POST'])
def update_authors_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_data = [obj['new']['first_name'],
                obj['new']['last_name']]
    query = DBMethods().get_query(AuthorData).filter(AuthorData.first_name.contains(obj['old']['first_name']),
                                                     AuthorData.last_name.contains(obj['old']['last_name']))
    for m in query:
        DBMethods().update_authors_data(m.id, new_data)
    l = []
    query = DBMethods().get_query(AuthorData).filter(AuthorData.first_name.contains(obj['new']['first_name']),
                                                     AuthorData.last_name.contains(obj['new']['last_name']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@authorsDataAPI.route('/add-new', methods=['POST'])
def add_new_authors_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    d = AuthorData(first_name=obj['first_name'], last_name=obj['last_name'])

    DBMethods().add_entity(d)

    query = DBMethods().get_query(AuthorData).filter(AuthorData.first_name.contains(obj['first_name']),
                                                     AuthorData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "authors_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

