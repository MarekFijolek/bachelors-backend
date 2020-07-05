# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shared.db import db
from models import Tag, MentionsInFile, Excerpt
from tags_search import get_all_tag_data
import os

# App init
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DOCUMENTATION_DIR'] = 'example_doc'

# Modules
db.init_app(app)

# Models

# Schema Objects
# TO DO

# Routes
# TO DO

def populate():
    all_tag_data = get_all_tag_data(app.config['DOCUMENTATION_DIR'])
    db.create_all()

    db.session.add_all(all_tag_data['tags'])
    db.session.add_all(all_tag_data['mentions'])
    db.session.add_all(all_tag_data['excerpts'])

    db.session.commit()

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == 'main':
    app.run()