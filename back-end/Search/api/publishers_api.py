import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

PublishersAPI = Blueprint('publishers', __name__)


def make_json(obj):
    return {
        "name": obj.name
    }


@PublishersAPI.route('/all', methods=['POST'])
def get_publishers_data_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(Publishers)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@PublishersAPI.route('/id', methods=['POST'])
def get_publishers_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Publishers).filter(Publishers.id.contains(obj['id']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@PublishersAPI.route('/name', methods=['POST'])
def get_publishers_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@PublishersAPI.route('/delete', methods=['POST'])
def delete_publishers_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['name']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(AuthorData, m.id)
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@PublishersAPI.route('/update', methods=['POST'])
def update_publishers():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    new_data = [obj['new']['name']]
    query = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['old']['name']))
    for m in query:
        DBMethods().update_authors_data(m.id, new_data)
    l = []
    query = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['new']['name']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@PublishersAPI.route('/add-new', methods=['POST'])
def add_new_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    d = Publishers(name=obj['name'])

    DBMethods().add_entity(d)

    query = DBMethods().get_query(Publishers).filter(Publishers.name.contains(obj['name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "publishers": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

