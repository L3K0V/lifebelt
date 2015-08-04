from lifebelt import db

from lifebelt.mod_users.models import User
from lifebelt.mod_assignments.models import Assignment

from datetime import datetime


class Course(db.Document):
    initials = db.StringField(max_length=8)
    fullname = db.StringField(max_length=64)
    description = db.StringField(max_length=4096)
    year = db.IntField(min_value=2015)
    users = db.ListField(db.DictField())
    assignments = db.EmbeddedDocumentListField(Assignment)

    date_created = db.DateTimeField()
    date_modified = db.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        self.modified_date = datetime.now()
        return super(Course, self).save(*args, **kwargs)
