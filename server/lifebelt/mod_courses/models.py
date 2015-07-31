from lifebelt import db
from lifebelt import app

from lifebelt.mod_users.models import User


class Course(db.Document):
    initials = db.StringField(max_length=16)
    fullname = db.StringField(max_length=64)
    description = db.StringField(max_length=2048)
    year = db.IntField(min_value=2015)
    students = db.ListField(db.ReferenceField(User))
    teachers = db.ListField(db.ReferenceField(User))
