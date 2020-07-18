from app import create_app, db
from app.models import Tag, MentionsInFile, Excerpt, Version
from app.tags_search import get_all_tag_data_and_stamp_version
from app.docs_repo import DocsRepo
from app.schemas import schema

from flask_graphql import GraphQLView
from apscheduler.schedulers.background import BackgroundScheduler

import click
import os
import time
import atexit

app = create_app()
docs_repo = DocsRepo(app.config['DOCUMENTATION_DIR'], app.config['DOCUMENTATION_URI'])

app.add_url_rule(
    '/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

def update_documentation_and_db():
    if not docs_repo.is_up_to_date():
        print(">> New update in documentation detected! Updating.")
        docs_repo.update()
        insert_tag_data_to_db()
    else:
        print(">> No updates in documentation")
    

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

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_documentation_and_db, trigger="interval", minutes=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())