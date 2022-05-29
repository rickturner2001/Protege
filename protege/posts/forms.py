from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField    
from flask_wtf.file import FileField, FileAllowed   
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    video = FileField('Video', validators=[FileAllowed(['mp4', 'mov'])])
    source = StringField("Video Source URL")
    category = StringField("Category")
    submit = SubmitField('Share')

