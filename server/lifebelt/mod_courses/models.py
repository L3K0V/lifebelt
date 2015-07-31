from lifebelt import db

from lifebelt.mod_users.models import User

from datetime import datetime


class Course(db.Document):
    initials = db.StringField(max_length=16)
    fullname = db.StringField(max_length=64)
    description = db.StringField(max_length=2048)
    year = db.IntField(min_value=2015)
    users = db.ListField(db.DictField())
    date_modified = db.DateTimeField(default=datetime.now)
