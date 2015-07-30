from lifebelt import db
from lifebelt import app

from lifebelt.mod_users.models import User

from sqlalchemy.ext.associationproxy import association_proxy


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(8), index=True)
    fullname = db.Column(db.String(64))
    description = db.Column(db.String(2048))
    year = db.Column(db.Integer)
    users = association_proxy('course_users', 'user')

    def to_json(self):
        result = {
            'id': self.id,
            'initias': self.initials,
            'fullname': self.fullname,
            'description': self.description,
            'year': self.year
        }

        return result


class CourseUser(db.Model):
    __tablename__ = 'course_user'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    user_role = db.Column(db.String(16))

    course = db.relationship(Course,
                             backref=db.backref('course_users'),
                             cascade='all, delete-orphan', single_parent=True)

    user = db.relationship(User)

    def __init__(self, user=None, course=None, user_role=None):
        self.user = user
        self.course = course
        self.user_role = user_role
