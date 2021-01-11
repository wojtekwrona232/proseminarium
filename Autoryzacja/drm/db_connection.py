from mongoengine import connection as conn_db


def db_open_con():
    conn_db.connect('authenticationMicroservice', host='localhost', port=27017)


def db_close():
    conn_db.disconnect()
