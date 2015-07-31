from lifebelt import db

from datetime import datetime


class Announcement(db.EmbeddedDocument):
    author = db.DictField()
    announcement = db.StringField(max_length=512)
    announcedOn = db.DateTimeField(default=datetime.now)

    comments = db.ListField(db.EmbeddedDocument(AnnoucementComment))


class AnnoucementComment(db.EmbeddedDocument):
    author = db.DictField()
    comment = db.StringField(max_length=512, required=True)
    commentedOn = db.DateTimeField(default=datetime.now)
