from lifebelt import db

from datetime import datetime


class Assignment(db.EmbeddedDocument):
    name = db.StringField(max_length=256, required=True)
    description = db.StringField(max_length=2048, required=True)
    type = db.StringField(max_length=32, required=True)
    startOn = db.DateTimeField(default=datetime.now)
    endOn = db.DateTimeField(default=datetime.now() + datetime.timedelta(days=5))
    target = db.ListField(db.StringField(max_length=16))

    submissions = db.ListField(db.EmbeddedDocument(Submission))


class Submission(db.EmbeddedDocument):
    author = db.DictField()
    description = db.StringField(max_length=128)
    submittedOn = db.DateTimeField(default=datetime.now)
    pullRequest = db.URLField(verify_exist=True)
    files = db.ListField(db.DictField())
    grade = db.DecimalField(defailt=0)

    reviews = db.ListField(db.EmbeddedDocument(Review))


class Review(db.EmbeddedDocument):
    author = db.DictField()
    description = db.StringField(max_length=512)
    points = db.DecimalField(required=True)
    reviewedOn = db.DateTimeField(default=datetime.now)
