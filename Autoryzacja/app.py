from functools import wraps

from bson import ObjectId
from flask import Flask, render_template, session, url_for, redirect, request, flash, jsonify
from api import accounts_api, libraries_api
from drm.Accounts import Account
import drm.db_connection as db
import hashlib
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\x89u\xf7M\xf03\xcb\x1b\xc6#\xd2"\x8b\xf8\xb7'

app.register_blueprint(libraries_api.libApi, url_prefix='/api/v1/resources/libraries')
app.register_blueprint(accounts_api.accApi, url_prefix='/api/v1/resources/accounts')


@app.route('/account/login')
def login():
    return render_template('login.html')


@app.route('/account/login', methods=['POST'])
def login_user():
    db.db_open_con()
    username = request.form['username']
    password = hashlib.md5(str(request.form['password']).encode('utf8')).hexdigest()
    is_reader = request.form['account_type']
    try:
        acc = Account.objects(login=username).get()
        if not acc:
            raise Exception(render_template('login.html', error='Invalid credentials!'))
        if acc.account_type == is_reader:
            if acc.password == password:
                session['username'] = username
                flash('You were successfully logged in')
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error=True)
        else:
            return render_template('login.html', error=True)
    except:
        return render_template('login.html', error=True)
    finally:
        db.db_close()


@app.route('/account/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')


# need privilege to register an employee
@app.route('/register/user', methods=['POST'])
def register_user():
    return 'Register user'


# need privilege to register an employee
@app.route('/register/emp', methods=['POST'])
def register_employee():
    return 'Register employee'


if __name__ == '__main__':
    app.run(debug=True)

