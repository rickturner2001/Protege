from protege import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}... {self.profile_image}"

class Post(db.Model):
# Setup the relationship to the User table
    users = db.relationship(User)
    # Model for the  Posts on Website
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_video = db.Column(db.String(140), nullable=True)
    post_video_url = db.Column(db.String(140), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    thumbnail = db.Column(db.String(140), nullable=True)
    actors = db.Column(db.String(500), nullable=True)
    is_leak = db.Column(db.Boolean, nullable=True)
    
    def __init__(self, title, user_id, post_video, post_video_url, category, thumbnail, actors, is_leak):
        self.title = title
        self.user_id =user_id
        self.post_video = post_video
        self.post_video_url = post_video_url
        self.category = category
        self.thumbnail = thumbnail
        self.actors = actors
        self.is_leak = is_leak
        
    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title} ... Video: {self.post_video or self.post_video_url}"