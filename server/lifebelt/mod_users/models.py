from lifebelt import db
from lifebelt import app
from lifebelt import login_serializer

from flask.ext.login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    github = db.Column(db.String(48), index=True, unique=True)
    github_token = db.Column(db.String(256))
    avatar_url = db.Column(db.String(256))
    email = db.Column(db.String(64), index=True, unique=True)
    fullname = db.Column(db.String(64))
    role = db.Column(db.String(16))
    student_grade = db.Column(db.Integer)
    student_class = db.Column(db.String(8))
    student_number = db.Column(db.Integer)

    def get_role(self):
        return self.role

    def get_auth_token(self):
        data = [str(self.id), self.github_token]
        return login_serializer.dumps(data)

    def to_json(self):
        result = {
            'id': self.id,
            'role': self.role,
            'fullname': self.fullname,
            'github': self.github,
            'avatar_url': self.avatar_url,
            'email': self.email,
            'details': {
                'grade': self.student_grade,
                'class': self.student_class,
                'number': self.student_number
            }
        }

        return result
