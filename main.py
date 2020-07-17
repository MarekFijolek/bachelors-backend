from app import create_app, db
from app.models import Tag, MentionsInFile, Excerpt
from app.tags_search import get_all_tag_data
import click
import os

app = create_app()

def populate():
    all_tag_data = get_all_tag_data(app.config['DOCUMENTATION_DIR'])
    db.create_all()

    db.session.add_all(all_tag_data['tags'])
    db.session.add_all(all_tag_data['mentions'])
    db.session.add_all(all_tag_data['excerpts'])

    db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Tag=Tag, MentionsInFile=MentionsInFile, Excerpt=Excerpt)