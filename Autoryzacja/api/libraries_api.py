import datetime
import json
from bson import ObjectId
from flask import Blueprint, request
from drm import db_connection as db
from drm.Libraries import Library

libApi = Blueprint('libraries', __name__)


@libApi.route('/single', methods=['POST'])
def single_library():
    obj = json.loads(request.data, strict=False)
    lib_id = obj['id']
    db.db_open_con()
    lib = Library.objects.get(_id=ObjectId(lib_id))
    library = {
        "name": lib.name,
        "address": lib.address,
        "city": lib.city,
    }
    db.db_close()
    return json.dumps(library, ensure_ascii=False, indent=4).encode('utf8')


@libApi.route('/all', methods=['POST'])
def all_libraries():
    db.db_open_con()
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    libraries = []
    for libs in Library.objects:
        library = {
            "name": libs.name,
            "address": libs.address,
            "city": libs.city,
        }
        libraries.append(library)

    file = {
        "meta": meta,
        "libraries": libraries
    }
    db.db_close()
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@libApi.route('/edit', methods=['POST'])
def edit_library():
    obj = json.loads(request.data, strict=False)
    l_id = obj['id']
    name = obj['name']
    address = obj['address']
    city = obj['city']

    db.db_open_con()
    now = datetime.datetime.now()
    try:
        Library.objects.get(_id=ObjectId(l_id)).update(name=name, address=address, city=city)
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Library has been modified successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Library has not been modified successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    finally:
        db.db_close()


@libApi.route('/new', methods=['POST'])
def add_new_library():
    obj = json.loads(request.data, strict=False)
    db.db_open_con()

    name = obj['name']
    address = obj['address']
    city = obj['city']

    now = datetime.datetime.now()
    try:
        Library(name=name, address=address, city=city).save()
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'New library added successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Failed to add new library'
        }, ensure_ascii=False, indent=4).encode('utf8')
    finally:
        db.db_close()


@libApi.route('/remove', methods=['POST'])
def remove_library():
    obj = json.loads(request.data, strict=False)
    db.db_open_con()

    name = obj['name']
    address = obj['address']
    city = obj['city']

    now = datetime.datetime.now()
    try:
        lib = Library.objects(name=name, address=address, city=city).get()
        Library(_id=lib.pk).delete()
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Library removed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Failed to remove library'
        }, ensure_ascii=False, indent=4).encode('utf8')
    finally:
        db.db_close()
