from bson import ObjectId
from flask import Flask, request, jsonify, make_response, session
from mongoengine import connection as conn_db
from api import accounts_api, libraries_api
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from orm import *
import datetime
import json
import jwt
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\x89u\xf7M\xf03\xcb\x1b\xc6#\xd2"\x8b\xf8\xb7'

app.register_blueprint(libraries_api.libApi, url_prefix='/api/v1/resources/libraries')
app.register_blueprint(accounts_api.accApi, url_prefix='/api/v1/resources/accounts')


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
            db = DBMethods()
            current_user = db.get_query(Accounts).filter_by(id=data['id']).first()
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
    db = DBMethods()
    users = db.get_all(Accounts)
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'id': str(user.id),
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

    if not auth or not auth.get('login') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401
        )

    db = DBMethods()
    user = db.get_query(Accounts).filter_by(login=auth.get('login')).first()
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': str(user.login),
            'exp': datetime.datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        session['username'] = user.login
        # return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
        file = {
            "token": token.decode('utf-8')
        }
        return jsonify(file), 201
        # returns 403 if password is wrong
    return  make_response('Could not verify', 403)
    


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email, log = data.get('name'), data.get('email'), data.get('login')

    # checking for existing user

    db = DBMethods()
    user = False
    users = db.get_all(Accounts)
    for u in users:
        if str(u.email).__eq__(email) or str(u.login).__eq__(log):
            user = True
    if not user:
        acc = Accounts(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            login=data.get('login'),
            password=generate_password_hash(data.get('password')),
            library_id=data.get('library'),
            address=data.get('address'),
            city=data.get('city'),
            zip_code=data.get('zip_code'),
            date_created=datetime.datetime.now(),
            account_type=data.get('account_type')
        )
        db.add(acc)
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
    
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 6000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
