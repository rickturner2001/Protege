from email.mime import base
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
basedir = Path(__name__).resolve().parent

app.config['SECRET_KEY'] = "my_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + str(basedir) + "/data.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app, db)

from my_site.posts.views import post_blueprint
app.register_blueprint(post_blueprint, url_prefix='/posts')