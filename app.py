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

# with app.app_context():
#     db.create_all()

def populate():
    db.create_all()
    tag = Tag(tag_name='tag', occurences_count=2)
    db.session.add(tag)
    db.session.commit()
    # adoc1 = MentionsInFile


@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == 'main':
    app.run()