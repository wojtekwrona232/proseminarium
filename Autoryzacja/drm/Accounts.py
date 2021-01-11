from mongoengine import *
from drm import Libraries
import datetime


class Account(Document):
    _id = ObjectIdField(primary_key=True)
    first_name = StringField(max_length=256, required=True)
    last_name = StringField(max_length=256, required=True)
    login = StringField(max_length=256, required=True)
    password = StringField(max_length=256, required=True)
    email = StringField(max_length=256, required=True)
    library_id = ReferenceField(Libraries.Library, required=True)
    address = StringField(max_length=256, required=True)
    city = StringField(max_length=256, required=True)
    zip_code = StringField(max_length=8, required=True)
    date_created = DateTimeField(default=datetime.datetime, required=True)
    account_type = StringField(max_length=50, required=True)

    meta = {'collection': 'accounts'}
