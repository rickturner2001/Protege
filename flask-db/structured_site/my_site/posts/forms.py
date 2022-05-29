from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DelForm(FlaskForm):
    id = IntegerField("Id Number of Post to Remove: ", validators=[DataRequired()])
    submit = SubmitField("Remove Post")
