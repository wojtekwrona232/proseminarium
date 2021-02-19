from flask import Flask, render_template, request, make_response, jsonify, session, url_for, redirect, Response
import requests
import os
import json
import datetime
import calendar
import enum


class ReservationEnum(enum.Enum):
    W_REALIZACJI = 0
    W_TRANSPORCIE = 1
    GOTOWA_DO_ODBIORU = 2
    ANULOWANO = 3
    ODEBRANO = 4


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\x89u\xf7M\xf03\xcb\x1b\xc6#\xd2"\x8b\xf8\xb7'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

EMPLOYEE = 'EMPLOYEE'
READER = 'READER'


@app.route('/add-book-in-library', methods=['GET', 'POST'])
def add_book_in_library():
    if session.get('status') == EMPLOYEE:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books_json = get_books.json()
        if request.method == 'POST':
            isbn = request.form.get('book_isbn')
            count = request.form.get('book_count')
            for i in range(0, int(count)):
                make = {
                    "isbn": isbn,
                    "available": True
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-book-availability', data=json.dumps(make))
            return search_book()
        return render_template('addbooktolibrary.html', books=books_json['books'])


@app.route('/show-returned-book', methods=['GET'])
def show_returned_book():
    if session.get('status') == EMPLOYEE:
        data = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check_id'))
        get_check = requests.get(url=str(data))
        res_details = get_check.json()
        r = res_details[0]

        date_today = datetime.datetime.today()
        date_return_term = datetime.datetime.strptime(r['return_term'], '%Y-%m-%d')
        if date_today < date_return_term:
            penalty = 0.0
        else:
            days_after_term = date_today - date_return_term
            number_of_days = days_after_term.days
            if number_of_days == 0:
                penalty = 0.0
            elif number_of_days > 0:
                penalty = number_of_days * 0.3
            else:
                penalty = 0.0

        get_data = requests.post('http://10.1.0.110:6001/api/v1/search/isbn', data=json.dumps({'isbn': r['book']['isbn']}))
        book = get_data.json()
        return render_template('view_book_return_pracownik.html',
                               isbn=r['book']['isbn'],
                               title=book['books']['book']['title'],
                               authors=book['books']['authors'],
                               translators=book['books']['translators'],
                               publisher=book['books']['book']['publisher'],
                               published_year=book['books']['book']['year_published'],
                               edition_nr=book['books']['book']['edition_nr'],
                               reader_id=r['reader_id'],
                               check_out_date=r['check_out_date'],
                               return_term=r['return_term'],
                               return_date=r['return_date'],
                               penalty=penalty,
                               check_id=r['id'])
    return Response(status=403)


@app.route('/show-return-book', methods=['GET'])
def show_return_book():
    if session.get('status') == EMPLOYEE:
        data = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check_id'))
        get_check = requests.get(url=str(data))
        res_details = get_check.json()
        r = res_details[0]

        date_today = datetime.datetime.today()
        date_return_term = datetime.datetime.strptime(r['return_term'], '%Y-%m-%d')
        if date_today < date_return_term:
            penalty = 0.0
        else:
            days_after_term = date_today - date_return_term
            number_of_days = days_after_term.days
            if number_of_days == 0:
                penalty = 0.0
            elif number_of_days > 0:
                penalty = number_of_days * 0.3
            else:
                penalty = 0.0

        get_data = requests.post('http://10.1.0.110:6001/api/v1/search/isbn', data=json.dumps({'isbn': r['book']['isbn']}))
        book = get_data.json()
        return render_template('view_book_return_pracownik.html',
                               isbn=r['book']['isbn'],
                               title=book['books']['book']['title'],
                               authors=book['books']['authors'],
                               translators=book['books']['translators'],
                               publisher=book['books']['book']['publisher'],
                               published_year=book['books']['book']['year_published'],
                               edition_nr=book['books']['book']['edition_nr'],
                               reader_id=r['reader_id'],
                               check_out_date=r['check_out_date'],
                               return_term=r['return_term'],
                               return_date=r['return_date'],
                               penalty=penalty,
                               check_id=r['id'])
    return Response(status=403)


@app.route('/return-book', methods=['GET', 'POST'])
def return_book():
    if session.get('status') == EMPLOYEE:
        data = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check_id'))
        get_check = requests.get(url=str(data))
        res_details = get_check.json()
        r = res_details[0]

        date_today = datetime.datetime.today()
        date_return_term = datetime.datetime.strptime(r['return_term'], '%Y-%m-%d')
        if date_today < date_return_term:
            penalty = 0.0
        else:
            days_after_term = date_today - date_return_term
            number_of_days = days_after_term.days
            if number_of_days == 0:
                penalty = 0.0
            elif number_of_days > 0:
                penalty = number_of_days * 0.3
            else:
                penalty = 0.0

        make = {
            "id": r['id'],
            "reservation_id": r['reservation_id'],
            "reservation": {
                "id": r['reservation']['id'],
                "reservation_date": r['reservation']['reservation_date'],
                "pick_up_date": r['reservation']['pick_up_date'],
                "status": ReservationEnum.ODEBRANO.name
            },
            "book_id": r['book_id'],
            "book": {
                "id": r['id'],
                "isbn": r['book']['isbn'],
                "available": True
            },
            "reader_id": r['reader_id'],
            "employee_id": session.get('email'),
            "check_out_date": r['check_out_date'],
            "return_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
            "return_term": r['return_term'],
            "late_return_penalty": penalty
        }
        requests.post('http://10.1.0.120:8001/api/v1/update-check-out', data=json.dumps(make))

        return view_borrowed()
    return Response(status=403)


@app.route('/cancel-reservation', methods=['GET', 'POST'])
def cancel_reservation():
    if session.get('status') == EMPLOYEE:
        data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.args.get('res_id'))
        get_data = requests.get(url=str(data))
        reservation = get_data.json()

        data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check'))
        get_check = requests.get(url=str(data1))
        res_details = get_check.json()

        res = reservation[0]
        make = {
            "id": res['id'],
            "reservation_date": res['reservation_date'],
            "pick_up_date": res['pick_up_date'],
            "status": ReservationEnum.ANULOWANO.name
        }
        requests.post('http://10.1.0.120:8001/api/v1/update-reservation', data=json.dumps(make))
        return view_reservations()
    return Response(status=403)


@app.route('/borrow-reservation', methods=['GET', 'POST'])
def borrow_reservation():
    if session.get('status') == EMPLOYEE:
        data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.args.get('res_id'))
        get_data = requests.get(url=str(data))
        reservation = get_data.json()
        res = reservation[0]

        data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check'))
        get_check = requests.get(url=str(data1))
        res_details = get_check.json()
        r = res_details[0]

        make = {
            "id": r['id'],
            "reservation_id": res['id'],
            "reservation": {
                "id": res['id'],
                "reservation_date": res['reservation_date'],
                "pick_up_date": res['pick_up_date'],
                "status": ReservationEnum.ODEBRANO.name
            },
            "book_id": r['book_id'],
            "book": {
                "id": r['id'],
                "isbn": r['book']['isbn'],
                "available": False
            },
            "reader_id": r['reader_id'],
            "employee_id": session.get('email'),
            "check_out_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
            "return_date": None,
            "return_term": str(add_months(datetime.datetime.today(), 1).strftime('%Y-%m-%d')),
            "late_return_penalty": 0.0
        }
        requests.post('http://10.1.0.120:8001/api/v1/update-check-out', data=json.dumps(make))

        return view_reservations()
    return Response(status=403)


@app.route('/change-reservation-status', methods=['GET', 'POST'])
def change_reservation_status():
    if session.get('status') == EMPLOYEE:
        res_enum = ['W_REALIZACJI', 'W_TRANSPORCIE', 'GOTOWA_DO_ODBIORU', 'ANULOWANO']

        if request.method == 'POST':
            data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.form.get('res_id'))
            get_data = requests.get(url=str(data))
            reservation = get_data.json()

            data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.form.get('check_id'))
            get_check = requests.get(url=str(data1))
            res_details = get_check.json()

            res_stat = request.form.get('res_stat')
            res = reservation[0]
            make = {
                "id": res['id'],
                "reservation_date": res['reservation_date'],
                "pick_up_date": res['pick_up_date'],
                "status": res_enum[int(res_stat)-1]
            }
            requests.post('http://10.1.0.120:8001/api/v1/update-reservation', data=json.dumps(make))
            return view_reservations()

        data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.args.get('res_id'))
        get_data = requests.get(url=str(data))
        reservation = get_data.json()

        data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check'))
        get_check = requests.get(url=str(data1))
        res_details = get_check.json()

        return render_template('change_reservation_status.html', enum_status=res_enum, res=reservation[0], check=res_details[0])
    if session.get('status') == EMPLOYEE:
        res_enum = ['W_REALIZACJI', 'W_TRANSPORCIE', 'GOTOWA_DO_ODBIORU', 'ANULOWANO']

        if request.method == 'POST':
            data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.form.get('res_id'))
            get_data = requests.get(url=str(data))
            reservation = get_data.json()

            data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.form.get('check_id'))
            get_check = requests.get(url=str(data1))
            res_details = get_check.json()

            res_stat = request.form.get('res_stat')
            res = reservation[0]
            make = {
                "id": res['id'],
                "reservation_date": res['reservation_date'],
                "pick_up_date": res['pick_up_date'],
                "status": res_enum[int(res_stat)-1]
            }
            requests.post('http://10.1.0.120:8001/api/v1/update-reservation', data=json.dumps(make))
            return view_reservations()

        data = str('http://10.1.0.120:8001/api/v1/get-reservations/id/') + str(request.args.get('res_id'))
        get_data = requests.get(url=str(data))
        reservation = get_data.json()

        data1 = str('http://10.1.0.120:8001/api/v1/get-check-out/id/') + str(request.args.get('check'))
        get_check = requests.get(url=str(data1))
        res_details = get_check.json()

        return render_template('change_reservation_status.html', enum_status=res_enum, res=reservation[0], check=res_details[0])
    return Response(status=403)


@app.route('/view-reservations', methods=['GET', 'POST'])
def view_reservations():
    if session.get('status') == EMPLOYEE:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_check_outs = requests.get('http://10.1.0.120:8001/api/v1/get-check-outs/all')
        book_lib = get_check_outs.json()

        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        return render_template('view_reservations_pracownik.html', checks=book_lib, books=books['books'], readers=readers['accounts'])
    if session.get('status') == READER:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_check_outs = requests.get('http://10.1.0.120:8001/api/v1/get-check-outs/all')
        book_lib = get_check_outs.json()

        return render_template('view_reservations_user.html', checks=book_lib, books=books['books'])
    return Response(status=403)


@app.route('/view-borrowed', methods=['GET', 'POST'])
def view_borrowed():
    if session.get('status') == EMPLOYEE:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_check_outs = requests.get('http://10.1.0.120:8001/api/v1/get-check-outs/all')
        book_lib = get_check_outs.json()

        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        return render_template('view_borrowed_pracownik.html', checks=book_lib, books=books['books'], readers=readers['accounts'])
    if session.get('status') == READER:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_check_outs = requests.get('http://10.1.0.120:8001/api/v1/get-check-outs/all')
        book_lib = get_check_outs.json()

        return render_template('view_borrowed_user.html', checks=book_lib, books=books['books'])
    return Response(status=403)


@app.route('/reserve-book-lat', methods=['GET', 'POST'])
def reserve_book_alt():
    if session.get('status') == EMPLOYEE:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        book = request.args.get('book')
        if request.method == 'POST':
            reader = request.form.get('reader')
            book_r = request.form.get('book')
            pick_up_date = request.form.get('pick_up_date')
            emp_id = session.get('email')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book_r and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make_resveration = {
                    "reservation_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "pick_up_date": str(pick_up_date),
                    "status": ReservationEnum.W_REALIZACJI.name
                }
                get_response = requests.post('http://10.1.0.120:8001/api/v1/add-reservation', data=json.dumps(make_resveration))
                reservation = get_response.json()

                make_check_out = {
                    "reservation_id": reservation['id'],
                    "reservation": {
                        "reservation_date": reservation['reservation_date'],
                        "pick_up_date": reservation['pick_up_date'],
                        "status": reservation['status']
                    },
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book_r,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": emp_id,
                    "check_out_date": None,
                    "return_date": None,
                    "return_term": None,
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make_check_out))
            return view_reservations()
        return render_template('reserve_pracownik2.html', readers=readers['accounts'], book=book)
    if session.get('status') == READER:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        book_r = request.args.get('book')
        if request.method == 'POST':
            reader = session.get('email')
            book_r = request.form.get('book')
            pick_up_date = request.form.get('pick_up_date')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book_r and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make_resveration = {
                    "reservation_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "pick_up_date": str(pick_up_date),
                    "status": ReservationEnum.W_REALIZACJI.name
                }
                get_response = requests.post('http://10.1.0.120:8001/api/v1/add-reservation', data=json.dumps(make_resveration))
                reservation = get_response.json()

                make_check_out = {
                    "reservation_id": reservation['id'],
                    "reservation": {
                        "reservation_date": reservation['reservation_date'],
                        "pick_up_date": reservation['pick_up_date'],
                        "status": reservation['status']
                    },
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book_r,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": None,
                    "check_out_date": None,
                    "return_date": None,
                    "return_term": None,
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make_check_out))
            return view_reservations()
        return render_template('reserve_user.html', books=books['books'], book=book_r)
    return Response(status=403)


@app.route('/reserve-book', methods=['GET', 'POST'])
def reserve_book():
    if session.get('status') == EMPLOYEE:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        if request.method == 'POST':
            reader = request.form.get('reader')
            book = request.form.get('book')
            pick_up_date = request.form.get('pick_up_date')
            emp_id = session.get('email')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make_resveration = {
                    "reservation_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "pick_up_date": str(pick_up_date),
                    "status": ReservationEnum.W_REALIZACJI.name
                }
                get_response = requests.post('http://10.1.0.120:8001/api/v1/add-reservation', data=json.dumps(make_resveration))
                reservation = get_response.json()

                make_check_out = {
                    "reservation_id": reservation['id'],
                    "reservation": {
                        "reservation_date": reservation['reservation_date'],
                        "pick_up_date": reservation['pick_up_date'],
                        "status": reservation['status']
                    },
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": emp_id,
                    "check_out_date": None,
                    "return_date": None,
                    "return_term": None,
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make_check_out))
            return render_template('reserve_pracownik.html', readers=readers['accounts'], books=books['books'])
        return render_template('reserve_pracownik.html', readers=readers['accounts'], books=books['books'])
    if session.get('status') == READER:
        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        if request.method == 'POST':
            reader = session.get('email')
            book = request.form.get('book')
            pick_up_date = request.form.get('pick_up_date')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make_resveration = {
                    "reservation_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "pick_up_date": str(pick_up_date),
                    "status": ReservationEnum.W_REALIZACJI.name
                }
                get_response = requests.post('http://10.1.0.120:8001/api/v1/add-reservation', data=json.dumps(make_resveration))
                reservation = get_response.json()

                make_check_out = {
                    "reservation_id": reservation['id'],
                    "reservation": {
                        "reservation_date": reservation['reservation_date'],
                        "pick_up_date": reservation['pick_up_date'],
                        "status": reservation['status']
                    },
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": None,
                    "check_out_date": None,
                    "return_date": None,
                    "return_term": None,
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make_check_out))
            return render_template('reserve_user.html', books=books['books'])
        return render_template('reserve_user.html', books=books['books'])
    return Response(status=403)


@app.route('/borrow-book-alt', methods=['GET', 'POST'])
def borrow_book_alt():
    if session.get('status') == EMPLOYEE:
        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        book = request.args.get('book')

        if request.method == 'POST':
            reader = request.form.get('reader')
            book_r = request.form.get('book')
            emp_id = session.get('email')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book_r and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make = {
                    "reservation_id": None,
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book_r,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": emp_id,
                    "check_out_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "return_date": None,
                    "return_term": str(add_months(datetime.datetime.today(), 1).strftime('%Y-%m-%d')),
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make))
            return view_borrowed()
        return render_template('borrow_pracownik2.html', readers=readers['accounts'], book=book)
    return Response(status=403)


@app.route('/borrow-book', methods=['GET', 'POST'])
def borrow_book():
    if session.get('status') == EMPLOYEE:
        get_readers = requests.post('http://10.1.0.111:6000/api/v1/resources/accounts/all')
        readers = get_readers.json()

        get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
        books = get_books.json()

        get_book_lib = requests.get('http://10.1.0.120:8001/api/v1/get-books-availability/all')
        book_lib = get_book_lib.json()

        if request.method == 'POST':
            reader = request.form.get('reader')
            book = request.form.get('book')
            emp_id = session.get('email')

            book_id = -1
            for i in book_lib:
                if i['isbn'] == book and i['available'] is True:
                    book_id = i['id']
                    break

            if book_id > 0:
                make = {
                    "reservation_id": None,
                    "book_id": book_id,
                    "book": {
                        "id": book_id,
                        "isbn": book,
                        "available": False
                    },
                    "reader_id": reader,
                    "employee_id": emp_id,
                    "check_out_date": str(datetime.datetime.today().strftime('%Y-%m-%d')),
                    "return_date": None,
                    "return_term": str(add_months(datetime.datetime.today(), 1).strftime('%Y-%m-%d')),
                    "late_return_penalty": 0.0
                }
                requests.post('http://10.1.0.120:8001/api/v1/add-check-out', data=json.dumps(make))
            return render_template('borrow_pracownik.html', readers=readers['accounts'], books=books['books'])
        return render_template('borrow_pracownik.html', readers=readers['accounts'], books=books['books'])
    return Response(status=403)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if session.get('status') == EMPLOYEE:
        get_publishers = requests.post('http://10.1.0.110:6001/api/v1/publishers/all')
        publishers = get_publishers.json()

        get_authors = requests.post('http://10.1.0.110:6001/api/v1/authors-data/all')
        authors = get_authors.json()

        get_translators = requests.post('http://10.1.0.110:6001/api/v1/translators-data/all')
        translators = get_translators.json()

        if request.method == 'POST':
            isbn = request.form.get('isbn')
            title = request.form.get('title')
            publisher = request.form.get('publisher')
            publish_year = request.form.get('publish_year')
            edition = request.form.get('edition')
            authors_list = request.form.getlist('itemsAuthorsData')
            translators_list = request.form.getlist('itemsTranslatorsData')

            authors_ids = []
            translators_ids = []

            for i in authors_list:
                authors_ids.append(i)
            for i in translators_list:
                translators_ids.append(i)

            publisher_name = requests.post('http://10.1.0.110:6001/api/v1/publishers/id', data=json.dumps({'id': publisher}))
            pub = publisher_name.json()

            make_json = {
                'isbn': isbn,
                'title': title,
                'publisher_id': pub['publishers']['id'],
                'year_published': publish_year,
                'edition_nr': edition
            }
            book = requests.post('http://10.1.0.110:6001/api/v1/books/add-new', data=json.dumps(make_json))
            book_response = book.json()

            for a in authors_ids:
                j = {
                    'id': book_response['Books']['id'],
                    'author_id': a
                }
                requests.post('http://10.1.0.110:6001/api/v1/authors/add-new', data=json.dumps(j))

            for a in translators_ids:
                j = {
                    'id': book_response['Books']['id'],
                    'translator_id': a
                }
                requests.post('http://10.1.0.110:6001/api/v1/translators/add-new', data=json.dumps(j))

            return render_template('addbook.html', publishers=publishers['publishers'], authors=authors['authors_data'], translators=translators['translators_data'])
        return render_template('addbook.html', publishers=publishers['publishers'], authors=authors['authors_data'], translators=translators['translators_data'])
    return Response(status=403)


@app.route('/add-author', methods=['GET', 'POST'])
def add_author():
    if session.get('status') == EMPLOYEE:
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            make_json = {
                'first_name': first_name,
                'last_name': last_name
            }
            requests.post('http://10.1.0.110:6001/api/v1/authors-data/add-new', data=json.dumps(make_json))
            return render_template('addauthor.html')
        return render_template('addauthor.html')
    return Response(status=403)


@app.route('/add-translator', methods=['GET', 'POST'])
def add_translator():
    if session.get('status') == EMPLOYEE:
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            make_json = {
                'first_name': first_name,
                'last_name': last_name
            }
            requests.post('http://10.1.0.110:6001/api/v1/translators-data/add-new', data=json.dumps(make_json))
            return render_template('addtranslator.html')
        return render_template('addtranslator.html')
    return Response(status=403)


@app.route('/add-publisher', methods=['GET', 'POST'])
def add_publisher():
    if session.get('status') == EMPLOYEE:
        if request.method == 'POST':
            publisher_name = request.form.get('publisher_name')
            make_json = {
                'name': publisher_name
            }
            requests.post('http://10.1.0.110:6001/api/v1/publishers/add-new', data=json.dumps(make_json))
            return render_template('addpublisher.html')
        return render_template('addpublisher.html')
    return Response(status=403)


@app.route('/parcel-status', methods=['GET', 'POST'])
def parcel_status():
    if session.get('status') == EMPLOYEE:
        return render_template('package_status.html')
    return Response(status=403)


@app.route('/show-book', methods=['GET'])
def show_book():
    if session.get('status') == EMPLOYEE:
        data = {'isbn': str(request.args.get('isbn'))}
        get_data = requests.post('http://10.1.0.110:6001/api/v1/search/isbn', data=json.dumps(data))
        book = get_data.json()
        return render_template('view_book_pracownik.html',
                               isbn=book['books']['book']['isbn'],
                               title=book['books']['book']['title'],
                               authors=book['books']['authors'],
                               translators=book['books']['translators'],
                               publisher=book['books']['book']['publisher'],
                               published_year=book['books']['book']['year_published'],
                               edition_nr=book['books']['book']['edition_nr'])
    if session.get('status') == READER:
        data = {'isbn': str(request.args.get('isbn'))}
        get_data = requests.post('http://10.1.0.110:6001/api/v1/search/isbn', data=json.dumps(data))
        book = get_data.json()
        return render_template('view_book_user.html',
                               isbn=book['books']['book']['isbn'],
                               title=book['books']['book']['title'],
                               authors=book['books']['authors'],
                               translators=book['books']['translators'],
                               publisher=book['books']['book']['publisher'],
                               published_year=book['books']['book']['year_published'],
                               edition_nr=book['books']['book']['edition_nr'])
    return Response(status=403)


@app.route('/search-book', methods=['GET', 'POST'])
def search_book():
    get_books = requests.get('http://10.1.0.110:6001/api/v1/search/all')
    books_json = get_books.json()
    if session.get('status') == EMPLOYEE:
        return render_template('search_book_pracownik.html', books=books_json['books'])
    if session.get('status') == READER:
        return render_template('search_book_user.html', books=books_json['books'])
    return Response(status=403)


@app.route('/register', methods=['GET', 'POST'])
def register():
    get_libraries = requests.post('http://10.1.0.111:6000/api/v1/resources/libraries/all')
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
        requests.post('http://10.1.0.111:6000/signup', data=send)
        return redirect(url_for('login'))
    return render_template('register.html', libraries=libraries['libraries'])


@app.route('/', methods=['GET', 'POST'])
def start():
    libraries = requests.post('http://10.1.0.111:6000/api/v1/resources/libraries/all')
    get_lib = libraries.json()
    for i in get_lib['libraries']:
        if i['id'] == 1:
            session['library_id'] = i['id']
            session['library_name'] = i['name']
            session['library_address'] = i['address']
            session['library_city'] = i['city']
            session['library_phone'] = '17 866 94 00'
    if session.get('token') is not None:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if session['status'] == EMPLOYEE:
        return render_template('afterlogon_pracownik.html',
                               first_name=session['first_name'],
                               last_name=session['last_name'])
    elif session['status'] == READER:
        return render_template('afterlogon_user.html',
                               first_name=session['first_name'],
                               last_name=session['last_name'])
    return Response(status=403)


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
            get_token = requests.post('http://10.1.0.111:6000/login', data=send)
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
            if token['status'] == EMPLOYEE:
                return redirect(url_for('home'))
            elif token['status'] == READER:
                return redirect(url_for('home'))
        else:
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    if session.get('token') is not None:
        session.pop('token', None)
        session.pop('status', None)
        session.pop('id', None)
        session.pop('first_name', None)
        session.pop('last_name', None)
        session.pop('email', None)
        return redirect(url_for('start'))
    return Response(status=403)


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 6050)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
