from my_site import db

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __init__(self, title, text) -> None:
        self.title = title
        self.text = text
    
    def __repr__(self) -> str:
        return f"{self.id} {self.title}"