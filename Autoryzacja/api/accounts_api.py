import json
import datetime
from bson import ObjectId
from flask import Blueprint, request
from orm import *


accApi = Blueprint('accounts', __name__)


def make_file_json(obj):
    return {
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "email": obj.email,
            "library": {
                    "name": obj.library_id.name,
                    "address": obj.library_id.address,
                    "city": obj.library_id.city,
                }
            ,
            "address": obj.address,
            "city": obj.city,
            "zip_code": obj.zip_code,
            "date_created": obj.date_created,
            "account_type": obj.account_type
    }


@accApi.route('/current', methods=['POST'])
def get_account():
    obj = json.loads(request.data, strict=False)
    db = DBMethods()
    curr_user = db.get_query(Accounts).filter_by(id=obj['id']).first()
    file = make_file_json(curr_user)
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@accApi.route('/all', methods=['POST'])
def all_accounts():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    db = DBMethods()
    query = db.get_all(Accounts)
    accounts = []
    for libs in query:
        accounts.append(make_file_json(libs))

    file = {
        "meta": meta,
        "accounts": accounts
    }
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@accApi.route('/new', methods=['POST'])
def new_account():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    try:
        db = DBMethods()
        acc = Accounts(
            first_name=obj['first_name'],
            last_name=obj['last_name'],
            email=obj['email'],
            login=obj['login'],
            password=obj['password'],
            library_id=obj['library'],
            address=obj['address'],
            city=obj['city'],
            zip_code=obj['zip_code'],
            date_created=now,
            account_type=obj['account_type']
        )
        db.add(acc)
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'The account has been created successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'The account could not be created successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')


@accApi.route('/edit', methods=['POST'])
def edit_account():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()

    try:
        db = DBMethods()
        acc_id = db.get_query(Accounts).filter_by(login=obj['login']).first()
        acc = Accounts(
            first_name=obj['first_name'],
            last_name=obj['last_name'],
            email=obj['email'],
            login=acc_id.login,
            password=obj['password'],
            library_id=acc_id.library_id,
            address=obj['address'],
            city=obj['city'],
            zip_code=obj['zip_code'],
            date_created=acc_id.date_created,
            account_type=acc_id.account_type
        )
        db.add(acc)
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Account has been modified successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Account has not been modified successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')


@accApi.route('/remove', methods=['POST'])
def remove_account():
    obj = json.loads(request.data, strict=False)

    now = datetime.datetime.now()
    db = DBMethods()
    acc_id = db.get_query(Accounts).filter_by(login=obj['login']).first()
    db.delete_id(Accounts, acc_id.id)
    try:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Account removed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Failed to remove account'
        }, ensure_ascii=False, indent=4).encode('utf8')
