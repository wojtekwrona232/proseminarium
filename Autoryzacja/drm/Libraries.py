from mongoengine import *


class Library(Document):
    _id = StringField(primary_key=True, required=True)
    name = StringField(max_length=256, required=True)
    address = StringField(max_length=256, required=True)
    city = StringField(max_length=256, required=True)

    meta = {'collection': 'libraries'}
