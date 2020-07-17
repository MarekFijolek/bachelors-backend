from app import create_app, db
from app.models import Tag, MentionsInFile, Excerpt, Version
from app.tags_search import get_all_tag_data_and_stamp_version
from docs_repo import DocsRepo
import click
import os

app = create_app()
docs_repo = DocsRepo(app.config['DOCUMENTATION_DIR'], app.config['DOCUMENTATION_URI'])

def update_documentation_and_db():
    if not docs_repo.is_up_to_date():
        docs_repo.update()
        insert_tag_data_to_db()

def insert_tag_data_to_db():
    version = Version(version_name=docs_repo.get_version())
    all_tag_data = get_all_tag_data_and_stamp_version(app.config['DOCUMENTATION_DIR'], version)

    db.create_all()

    db.session.add_all(all_tag_data['tags'])
    db.session.add_all(all_tag_data['mentions'])
    db.session.add_all(all_tag_data['excerpts'])
    db.session.add(version)

    db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Tag=Tag, MentionsInFile=MentionsInFile, Excerpt=Excerpt, Version=Version)