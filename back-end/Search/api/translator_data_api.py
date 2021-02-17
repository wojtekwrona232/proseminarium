import datetime
import json
from flask import Blueprint, request
from db.db_methods import *

translatorsDataAPI = Blueprint('translators-data', __name__)


def make_json(obj):
    return {
        "id": obj.id,
        "first_name": obj.first_name,
        "last_name": obj.last_name
    }


@translatorsDataAPI.route('/all', methods=['POST'])
def get_translators_data_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_all(TranslatorsData)
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/id', methods=['POST'])
def get_translators_data_id():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        },
        "title": "buyers with specified id"
    }
    query = DBMethods().get_query(TranslatorsData).filter_by(id=obj['id']).first()
    file = {
        "meta": meta,
        "translators_data": make_json(query)
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/first-name', methods=['POST'])
def get_translators_data_first_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.first_name.contains(obj['first_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/last-name', methods=['POST'])
def get_translators_data_last_name():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/delete', methods=['POST'])
def delete_translators_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.first_name.contains(obj['first_name']),
                                                          TranslatorsData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
        DBMethods().delete_id(TranslatorsData, m.id)
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/update', methods=['POST'])
def update_translators_data():
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
    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.first_name.contains(obj['old']['first_name']),
                                                          TranslatorsData.last_name.contains(obj['old']['last_name']))
    for m in query:
        DBMethods().update_translators_data(m.id, new_data)
    l = []
    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.first_name.contains(obj['new']['first_name']),
                                                          TranslatorsData.last_name.contains(obj['new']['last_name']))
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@translatorsDataAPI.route('/add-new', methods=['POST'])
def add_new_translators_data():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    d = TranslatorsData(first_name=obj['first_name'], last_name=obj['last_name'])

    DBMethods().add_entity(d)

    query = DBMethods().get_query(TranslatorsData).filter(TranslatorsData.first_name.contains(obj['first_name']),
                                                          TranslatorsData.last_name.contains(obj['last_name']))
    l = []
    for m in query:
        l.append(make_json(m))
    file = {
        "meta": meta,
        "translators_data": l
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')

