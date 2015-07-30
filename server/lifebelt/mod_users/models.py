from lifebelt import db
from lifebelt import app
from lifebelt import login_serializer

from flask.ext.login import UserMixin


class User(UserMixin, db.Document):

    github = db.StringField(max_length=32)
    github_token = db.StringField(max_length=256)
    avatar_url = db.URLField(max_length=256)
    email = db.EmailField()
    fullname = db.StringField(max_length=64)
    role = db.StringField(max_length=16)
    student_grade = db.IntField(min_value=8, max_value=12)
    student_class = db.StringField(max_length=3)
    student_number = db.IntField(min_value=1, max_value=42)

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
