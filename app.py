# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shared.db import db
from models import Tag, MentionsInFile, Excerpt
import os

# App init
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db.init_app(app)

# Models

# Schema Objects
# TO DO

# Routes
# TO DO

def populate_initial():
    db.create_all()

    tag = Tag(tag_name='tag', occurences_count=2)
    adoc1 = MentionsInFile(file_name='adoc1', occurences_in_file_count=1)
    adoc2 = MentionsInFile(file_name='adoc2', occurences_in_file_count=1)
    adoc1_mention = Excerpt(text=str('blabla'))
    adoc2_mention = Excerpt(text=str('sample text'))

    adoc1.excerpts.append(adoc1_mention)
    adoc2.excerpts.append(adoc2_mention)

    tag.mentions.extend([adoc1, adoc2])

    db.session.add(tag)
    db.session.add(adoc1)
    db.session.add(adoc2)
    db.session.add(adoc1_mention)
    db.session.add(adoc2_mention)

    db.session.commit()


@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == 'main':
    app.run()