import json
import datetime
from bson import ObjectId
from flask import Blueprint, request
from drm.Accounts import Account
from drm import db_connection as db


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
    db.db_open_con()
    curr_user = Account.objects.get(_id=ObjectId(obj['id']))
    file = make_file_json(curr_user)
    db.db_close()
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
    db.db_open_con()
    accounts = []
    for libs in Account.objects:
        accounts.append(make_file_json(libs))

    file = {
        "meta": meta,
        "accounts": accounts
    }
    db.db_close()
    return json.dumps(file, ensure_ascii=False, indent=4).encode('utf8')


@accApi.route('/new', methods=['POST'])
def new_account():
    obj = json.loads(request.data, strict=False)
    db.db_open_con()
    now = datetime.datetime.now()
    try:
        Account(
            _id=ObjectId(),
            first_name=obj['first_name'],
            last_name=obj['last_name'],
            email=obj['email'],
            login=obj['login'],
            password=obj['password'],
            library_id=ObjectId(obj['library']),
            address=obj['address'],
            city=obj['city'],
            zip_code=obj['zip_code'],
            date_created=now,
            account_type=obj['account_type']
        ).save()
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
    finally:
        db.db_close()


@accApi.route('/edit', methods=['POST'])
def edit_account():
    obj = json.loads(request.data, strict=False)
    db.db_open_con()
    now = datetime.datetime.now()

    try:
        Account.objects.get(_id=ObjectId(obj['id'])).update(
            first_name=obj['first_name'],
            last_name=obj['last_name'],
            email=obj['email'],
            address=obj['address'],
            city=obj['city'],
            zip_code=obj['zip_code']
        )
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
    finally:
        db.db_close()


@accApi.route('/edit/library', methods=['POST'])
def edit_account_library():
    obj = json.loads(request.data, strict=False)

    db.db_open_con()
    now = datetime.datetime.now()

    try:
        Account.objects.get(_id=ObjectId(obj['id'])).update(library_id=ObjectId(obj['library']))
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Library has been changed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Library has not been changed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    finally:
        db.db_close()


@accApi.route('/edit/password', methods=['POST'])
def edit_account_password():
    obj = json.loads(request.data, strict=False)

    db.db_open_con()
    now = datetime.datetime.now()
    try:
        Account.objects.get(_id=ObjectId(obj['id'])).update(password=obj['password'])
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Password has been changed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    except:
        return json.dumps({
            "new": {
                "date": str(now.date()),
                "time": now.strftime("%H:%M:%S")
            },
            'message': 'Password has not been changed successfully'
        }, ensure_ascii=False, indent=4).encode('utf8')
    finally:
        db.db_close()


@accApi.route('/remove', methods=['POST'])
def remove_account():
    obj = json.loads(request.data, strict=False)

    db.db_open_con()
    now = datetime.datetime.now()
    Account.objects(login=obj['login'], email=obj['email']).delete()
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
    finally:
        db.db_close()
