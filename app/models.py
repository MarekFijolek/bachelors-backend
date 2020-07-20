from . import db
from datetime import datetime

class Tag(db.Model):
    __tablename__ = 'tags'
    
    uuid = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(256), index=True)
    occurrences_count = db.Column(db.Integer)

    mentions = db.relationship('MentionsInFile', backref='tag')

    version_id = db.Column(db.Integer, db.ForeignKey('versions.uuid'))
    version = db.relationship("Version")

    def __repr__(self):
        return '<Tag %r>' % self.tag_name

class MentionsInFile(db.Model):
    __tablename__ = "mentions"

    uuid = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(256))
    occurrences_in_file_count = db.Column(db.Integer)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.uuid'))
    excerpts = db.relationship('Excerpt', backref='mention')

    version_id = db.Column(db.Integer, db.ForeignKey('versions.uuid'))
    version = db.relationship("Version")

    def __repr__(self):
        return '<Mentions of %r in file %r>' % (self.tag_id, self.file_name)

class Excerpt(db.Model):
    __tablename__ = "excerpts"

    uuid = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    mentions_in_file_id = db.Column(db.Integer, db.ForeignKey('mentions.uuid'))

    version_id = db.Column(db.Integer, db.ForeignKey('versions.uuid'))
    version = db.relationship("Version")

    def __repr__(self):
        return '<Excerpt %r in file %r>' % (self.uuid, self.mentions_in_file_id)

class Version(db.Model):
    __tablename__ = "versions"

    uuid = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(256), index=True, unique=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    tags = db.relationship("Tag", back_populates="version")
    mentions = db.relationship("MentionsInFile", back_populates="version")
    excerpts = db.relationship("Excerpt", back_populates="version")

    def __repr__(self):
        return '<Version %r>' % self.version_name