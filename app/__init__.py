from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import configs, Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    config = configs[Config.ENV]
    app.config.from_object(config)

    config.init_app(app)
    db.init_app(app)

    return app