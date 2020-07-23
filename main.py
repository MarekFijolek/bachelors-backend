from app import create_app, db
from app.models import Tag, MentionsInFile, Excerpt, Version
from app.tags_search import get_all_tag_data_and_stamp_version
from app.docs_repo import DocsRepo
from app.schemas import schema

from flask_graphql import GraphQLView
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

import click
import os
import atexit

app = create_app()
docs_repo = DocsRepo(app.config['DOCUMENTATION_DIR'], app.config['DOCUMENTATION_URI'])
CORS(app)

app.add_url_rule(
    '/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

def update_documentation_and_db():
    with app.app_context():
        docs_repo.update_versions_info()

        if not docs_repo.is_up_to_date():
            new_docs_versions = docs_repo.get_next_versions()

            for version in new_docs_versions:
                docs_repo.set_version(version)
                insert_tag_data_to_db()
                print(">> Updated documentation to version %s" % version)

def insert_tag_data_to_db():
    with app.app_context():
        version = Version(version_name=docs_repo.get_current_version())

        tags, mentions, excerpts = get_all_tag_data_and_stamp_version(app.config['DOCUMENTATION_DIR'], version)

        db.create_all()

        db.session.add_all(tags)
        db.session.add_all(mentions)
        db.session.add_all(excerpts)
        db.session.add(version)

        db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Tag=Tag, MentionsInFile=MentionsInFile, Excerpt=Excerpt, Version=Version)

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_documentation_and_db, trigger="interval", minutes=1)
scheduler.start()

update_documentation_and_db()

atexit.register(lambda: scheduler.shutdown())
