import datetime
import json
import requests
from flask import request, Blueprint
from db.db_methods import *

searchAPI = Blueprint('search', __name__)


def check_for_availability(book_id, url):
    response = requests.get(url=url)
    return response.json()


def make_book_json(obj):
    return {
        "id": obj.id,
        "isbn": obj.isbn,
        "title": obj.title,
        "publisher": obj.publisher.name,
        "year_published": obj.year_published,
        "edition_nr": obj.edition_nr
    }


def make_authors_json(obj):
    return {
        "first_name": obj.author.first_name,
        "last_name": obj.author.last_name
    }


def make_translators_json(obj):
    return {
        "first_name": obj.translator.first_name,
        "last_name": obj.translator.last_name
    }


def make_availability_json(lib_id, available):
    return {
        "library_id": lib_id,
        "available": available
    }


@searchAPI.route('/all', methods=['GET'])
def search_all():
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    books = []
    query = DBMethods().get_all(Books)
    for n in query:
        l2 = []
        query1 = DBMethods().get_query(Authors).filter(Authors.book_id == n.id)
        for m in query1:
            l2.append(make_authors_json(m))
        l3 = []
        query2 = DBMethods().get_query(Translators).filter(Translators.book_id == n.id)
        for m in query2:
            l3.append(make_translators_json(m))
        l4 = []

        link1 = 'http://10.1.0.120:8001/api/v1/get-book-availability/id/' + n.isbn
        am = check_for_availability(n.isbn, link1)
        if am:
            avail1 = 0
            for i in am:
                if i['available'] == True:
                    avail1 += 1
            l4.append(make_availability_json(1, avail1))
        
        link2 = 'http://10.1.0.121:8002/api/v1/get-book-availability/id/' + n.isbn
        am1 = check_for_availability(n.isbn, link2)
        
        if am1:
            avail2 = 0
            for i in am1:
                if i['available'] == True:
                    avail2 += 1
            l4.append(make_availability_json(2, avail2))
        
        b = {
            "book": make_book_json(n),
            "authors": l2,
            "translators": l3,
            "availability": l4
        }
        books.append(b)
    file = {
        "meta": meta,
        "books": books
    }
    return json.dumps(file, ensure_ascii=False, indent=1).encode('utf8')


@searchAPI.route('/title', methods=['POST'])
def title_search():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    books = []
    query = DBMethods().get_query(Books).filter(Books.title.like('%' + obj['title'] + '%'))
    for n in query:
        l2 = []
        query1 = DBMethods().get_query(Authors).filter(Authors.book_id == n.id)
        for m in query1:
            l2.append(make_authors_json(m))
        l3 = []
        query2 = DBMethods().get_query(Translators).filter(Translators.book_id == n.id)
        for m in query2:
            l3.append(make_translators_json(m))
        l4 = []

        link1 = 'http://10.1.0.120:8001/api/v1/get-book-availability/id/' + n.isbn
        am = check_for_availability(n.isbn, link1)
        if am:
            avail1 = 0
            for i in am:
                if i['available'] == True:
                    avail1 += 1
            l4.append(make_availability_json(1, avail1))
        
        link2 = 'http://10.1.0.121:8002/api/v1/get-book-availability/id/' + n.isbn
        am1 = check_for_availability(n.isbn, link2)
        
        if am1:
            avail2 = 0
            for i in am1:
                if i['available'] == True:
                    avail2 += 1
            l4.append(make_availability_json(2, avail2))
        
        b = {
            "book": make_book_json(n),
            "authors": l2,
            "translators": l3,
            "availability": l4
        }
        books.append(b)
    file = {
        "meta": meta,
        "books": books
    }
    return json.dumps(file, ensure_ascii=False, indent=1).encode('utf8')


@searchAPI.route('/isbn', methods=['POST'])
def isbn_search():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    n = DBMethods().get_query(Books).filter_by(isbn=obj['isbn']).first()
    l2 = []
    query1 = DBMethods().get_query(Authors).filter(Authors.book_id == n.id)
    for m in query1:
        l2.append(make_authors_json(m))
    l3 = []
    query2 = DBMethods().get_query(Translators).filter(Translators.book_id == n.id)
    for m in query2:
        l3.append(make_translators_json(m))
    
    l4 = []

    link1 = 'http://10.1.0.120:8001/api/v1/get-book-availability/id/' + n.isbn
    am = check_for_availability(n.isbn, link1)
    if am:
        avail1 = 0
        for i in am:
            if i['available'] == True:
                avail1 += 1
        l4.append(make_availability_json(1, avail1))
    
    link2 = 'http://10.1.0.121:8002/api/v1/get-book-availability/id/' + n.isbn
    am1 = check_for_availability(n.isbn, link2)
    if am1:
        avail2 = 0
        for i in am1:
            if i['available'] == True:
                avail2 += 1
        l4.append(make_availability_json(2, avail2))
    
    b = {
        "book": make_book_json(n),
        "authors": l2,
        "translators": l3,
        "availability": l4
    }
    file = {
        "meta": meta,
        "books": b
    }
    return json.dumps(file, ensure_ascii=False, indent=1).encode('utf8')


@searchAPI.route('/publisher', methods=['POST'])
def publisher_search():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    books = []
    query = DBMethods().get_query(Publishers).filter(Publishers.name == obj['publisher'])
    for b in query:
        query3 = DBMethods().get_query(Books).filter(Books.publisher_id == b.id)
        for n in query3:
            l2 = []
            query1 = DBMethods().get_query(Authors).filter(Authors.book_id == n.id)
            for m in query1:
                l2.append(make_authors_json(m))
            l3 = []
            query2 = DBMethods().get_query(Translators).filter(Translators.book_id == n.id)
            for m in query2:
                l3.append(make_translators_json(m))
            
            l4 = []

            link1 = 'http://10.1.0.120:8001/api/v1/get-book-availability/id/' + n.isbn
            am = check_for_availability(n.isbn, link1)
            if am:
                avail1 = 0
                for i in am:
                    if i['available'] == True:
                        avail1 += 1
                l4.append(make_availability_json(1, avail1))
            
            link2 = 'http://10.1.0.121:8002/api/v1/get-book-availability/id/' + n.isbn
            am1 = check_for_availability(n.isbn, link2)
            
            if am1:
                avail2 = 0
                for i in am1:
                    if i['available'] == True:
                        avail2 += 1
                l4.append(make_availability_json(2, avail2))
            
            b = {
                "book": make_book_json(n),
                "authors": l2,
                "translators": l3,
                "availability": l4
            }
            books.append(b)
    file = {
        "meta": meta,
        "books": books
    }
    return json.dumps(file, ensure_ascii=False, indent=1).encode('utf8')


@searchAPI.route('/author', methods=['POST'])
def author_search():
    obj = json.loads(request.data, strict=False)
    now = datetime.datetime.now()
    meta = {
        "export": {
            "date": str(now.date()),
            "time": now.strftime("%H:%M:%S")
        }
    }
    query1 = DBMethods().get_query(AuthorData).filter(
        AuthorData.first_name.like('%' + obj['first_name'] + '%'),
        AuthorData.last_name.like('%' + obj['last_name'] + '%'))

    books = []
    for b in query1:
        query2 = DBMethods().get_query(Authors).filter(Authors.author_id == b.id)
        for v in query2:
            query3 = DBMethods().get_query(Books).filter(Books.id == v.book_id)
            for n in query3:
                l2 = []
                query1 = DBMethods().get_query(Authors).filter(Authors.book_id == n.id)
                for m in query1:
                    l2.append(make_authors_json(m))
                l3 = []
                query2 = DBMethods().get_query(Translators).filter(Translators.book_id == n.id)
                for m in query2:
                    l3.append(make_translators_json(m))
                
                l4 = []

                link1 = 'http://10.1.0.120:8001/api/v1/get-book-availability/id/' + n.isbn
                am = check_for_availability(n.isbn, link1)
                if am:
                    avail1 = 0
                    for i in am:
                        if i['available'] == True:
                            avail1 += 1
                    l4.append(make_availability_json(1, avail1))
                
                link2 = 'http://10.1.0.121:8002/api/v1/get-book-availability/id/' + n.isbn
                am1 = check_for_availability(n.isbn, link2)
                
                if am1:
                    avail2 = 0
                    for i in am1:
                        if i['available'] == True:
                            avail2 += 1
                    l4.append(make_availability_json(2, avail2))
        
                b = {
                    "book": make_book_json(n),
                    "authors": l2,
                    "translators": l3,
                    "availability": l4
                }
                books.append(b)
    file = {
        "meta": meta,
        "books": books
    }
    return json.dumps(file, ensure_ascii=False, indent=1).encode('utf8')

