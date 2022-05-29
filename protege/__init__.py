from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = Path(__file__).resolve().parent
UPLOAD_FOLDER = basedir / 'static' / 'videos'

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + str(basedir) + "/data.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "users.login"

from protege.core.views import core
from protege.users.views import users
from protege.errors.handlers import error_pages
from protege.posts.views import posts

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(posts)