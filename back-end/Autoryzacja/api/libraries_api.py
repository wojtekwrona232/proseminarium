import datetime
import json
from bson import ObjectId
from flask import Blueprint, request
from orm import *

libApi = Blueprint('libraries', __name__)


@libApi.route('/single', methods=['POST'])
def single_library():
    obj = json.loads(request.data, strict=False)
    lib_id = obj['id']
    db = DBMethods()
    lib = db.get_query(Libraries).filter_by(id=lib_id).first()
    library = {
        "id": lib.id,
        "name": lib.name,
        "address": lib.address,
        "city": lib.city,
    }
    return json.dumps(library, ensure_ascii=False, indent=4).encode('utf8')


@libApi.route('/all', methods=['POST'])
def all_libraries():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    db = DBMethods()
    query = db.get_all(Libraries)
    libraries = []
    for libs in query:
        library = {
            "id": libs.id,
            "name": libs.name,
            "address": libs.address,
            "city": libs.city,
        }
        libraries.append(library)

    file = {
        "meta": meta,
        "libraries": libraries
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')
