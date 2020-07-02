from shared.db import db

class Tag(db.Model):
    __tablename__ = 'tags'
    
    uuid = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(256), index=True, unique=True)
    occurences_count = db.Column(db.Integer)

    mentions = db.relationship('MentionsInFile', backref='tag')

    def __repr__(self):
        return '<Tag %r>' % self.tag_name

class MentionsInFile(db.Model):
    __tablename__ = "mentions"

    uuid = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(256))
    occurences_in_file_count = db.Column(db.Integer)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.uuid'))
    excerpts = db.relationship('Excerpt', backref='mention')

    def __repr__(self):
        return '<Mentions of %r in file %r>' % (self.tag_id, self.file_name)

class Excerpt(db.Model):
    __tablename__ = "excerpts"

    uuid = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    mentions_in_file_id = db.Column(db.Integer, db.ForeignKey('mentions.uuid'))

    def __repr__(self):
        return '<Excerpt %r in file %r>' % (self.uuid, self.mentions_in_file_id)