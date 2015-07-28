from app import db
from app import app


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class User(Base):
    __tablename__ = 'user'

    github = db.Column(db.String(48), index=True, unique=True, nullable=False)
    github_token = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(16), nullable=False)
    student_grade = db.Column(db.Integer, nullable=True)
    student_class = db.Column(db.String(8), nullable=True)
    student_number = db.Column(db.Integer, nullable=True)

    def to_json(self):
        result = {
            'id': self.id,
            'role': self.role,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'github': self.github,
            'email': self.email,
            'details': {
                'grade': self.student_grade,
                'class': self.student_class,
                'number': self.student_number
            }
        }

        return result
