from bson import ObjectId
from flask import Flask, request, jsonify, make_response, session
from mongoengine import connection as conn_db
from api import accounts_api, libraries_api
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from enum import Enum
from mongoengine import *
import datetime
import json
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\x89u\xf7M\xf03\xcb\x1b\xc6#\xd2"\x8b\xf8\xb7'

app.register_blueprint(libraries_api.libApi, url_prefix='/api/v1/resources/libraries')
app.register_blueprint(accounts_api.accApi, url_prefix='/api/v1/resources/accounts')


def db_open_con():
    conn_db.connect('authenticationMicroservice', host='localhost', port=27017)


def db_close():
    conn_db.disconnect()


# Database ORMs
class AccountType(Enum):
    employee = 'EMPLOYEE'
    admin = 'EMPLOYEE_ADMIN'
    reader = 'READER'


class Library(Document):
    _id = StringField(primary_key=True, required=True)
    name = StringField(max_length=256, required=True)
    address = StringField(max_length=256, required=True)
    city = StringField(max_length=256, required=True)

    meta = {'collection': 'libraries'}


class Account(Document):
    _id = ObjectIdField(primary_key=True)
    first_name = StringField(max_length=256, required=True)
    last_name = StringField(max_length=256, required=True)
    login = StringField(max_length=256, required=True)
    password = StringField(max_length=256, required=True)
    email = StringField(max_length=256, required=True)
    library_id = ReferenceField(Library, required=True)
    address = StringField(max_length=256, required=True)
    city = StringField(max_length=256, required=True)
    zip_code = StringField(max_length=8, required=True)
    date_created = DateTimeField(default=datetime.datetime, required=True)
    account_type = StringField(max_length=50, required=True)

    meta = {'collection': 'accounts'}


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            db_open_con()
            current_user = Account.objects.get(_id=data['id'])
            db_close()
        except:
            return jsonify({'message': 'Token is invalid !!'}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    db_open_con()
    users = Account.objects
    db_close()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'id': str(user._id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

    return jsonify({'users': output})


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    db_open_con()
    user = Account.objects.get(email=auth.get('email'))
    db_close()
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': str(user._id),
            'exp': datetime.datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        session['username'] = user.login
        # return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
        file = {
            "token": token
        }
        return make_response(json.dumps(file, ensure_ascii=False, indent=4).encode('utf8'), 201)
        # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get('name'), data.get('email')

    # checking for existing user
    db_open_con()
    user = False
    users = Account.objects
    for u in users:
        if str(u.email).__eq__(email):
            user = True
    if not user:
        # database ORM object
        Account(
            _id=ObjectId(),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            login=data.get('login'),
            password=generate_password_hash(data.get('password')),
            library_id=ObjectId(data.get('library')),
            address=data.get('address'),
            city=data.get('city'),
            zip_code=data.get('zip_code'),
            date_created=datetime.datetime.now(),
            account_type=data.get('account_type')
        ).save()
        db_close()
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


# signup route
@app.route('/logout', methods=['DELETE'])
def logout():

    session.pop('username', None)
    return make_response('You are logged out.', 200)


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debuger shell
    # if you hit an error while running the server
    app.run(debug=True)
