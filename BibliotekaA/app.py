from flask import Flask, render_template, request, make_response, jsonify, session, url_for, redirect
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\x89u\xf7M\xf03\xcb\x1b\xc6#\xd2"\x8b\xf8\xb7'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/parcel-status', methods=['GET', 'POST'])
def parcel_status():
    return render_template('package_status.html')


@app.route('/search-book', methods=['GET', 'POST'])
def search_book():
    get_books = requests.get('http://127.0.0.1:6001/api/v1/search/all')
    books_json = get_books.json()
    if session.get('status') == 'EMPLOYEE':
        return render_template('search_book_pracownik.html', books=books_json['books'])
    elif session.get('status') == 'USER':
        return render_template('search_book_user.html', books=books_json['books'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    get_libraries = requests.post('http://127.0.0.1:6000/api/v1/resources/libraries/all')
    # print(get_libraries.json())
    libraries = get_libraries.json()

    if request.method == 'POST':
        send = {
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "email": request.form.get('email'),
            "login": request.form.get('login'),
            "password": request.form.get('password'),
            "library": request.form.get('library_id'),
            "address": request.form.get('address'),
            "city": request.form.get('city'),
            "zip_code": request.form.get('zipcode'),
            "account_type": "READER"
        }
        new_user = requests.post('http://127.0.0.1:6000/signup', data=send)
        return redirect(url_for('login'))
    return render_template('register.html', libraries=libraries['libraries'])


@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_f = request.form.get('login')
        password = request.form.get('password')
        if (login_f is not None or str(login_f).__len__() > 0) and (password is not None or str(password).__len__() > 0):
            send = {
                'login': str(login_f),
                'password': str(password)
            }
            get_token = requests.post('http://127.0.0.1:6000/login', data=send)
            if get_token.status_code != 201:
                message = {'message': 'Could not verify. Wrong password or username or the account does not exist'}
                return make_response(jsonify(message), 403)
            token = get_token.json()
            session['token'] = token['token']
            session['status'] = token['status']
            session['id'] = token['id']
            session['first_name'] = token['first_name']
            session['last_name'] = token['last_name']
            session['email'] = token['email']
            if token['status'] == 'EMPLOYEE':
                return render_template('afterlogon_pracownik.html', first_name=token['first_name'], last_name=token['last_name'])
            elif token['status'] == 'READER':
                return render_template('afterlogon_user.html', first_name=token['first_name'], last_name=token['last_name'])
        else:
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('token', None)
    session.pop('status', None)
    session.pop('id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
