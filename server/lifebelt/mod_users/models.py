from lifebelt import db
from lifebelt import login_serializer

from flask.ext.login import UserMixin

from datetime import datetime


class User(UserMixin, db.Document):

    github = db.StringField(max_length=32, unique=True)
    github_token = db.StringField(max_length=256, unique=True)
    avatar_url = db.URLField(max_length=256)
    email = db.EmailField(unique=True)
    fullname = db.StringField(max_length=64)
    role = db.StringField(max_length=16)
    details = db.DictField()
    courses = db.ListField(db.ReferenceField("Course"))
    date_modified = db.DateTimeField(default=datetime.now)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_role(self):
        return self.role

    def get_auth_token(self):
        data = [str(self.id), self.github_token]
        return login_serializer.dumps(data)
