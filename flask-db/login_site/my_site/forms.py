
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from my_site.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(Email())])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must match")])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")


    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(f"This email has already been registered")
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already taken")

class AddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DelForm(FlaskForm):
    id = IntegerField("Id Number of Post to Remove: ", validators=[DataRequired()])
    submit = SubmitField("Remove Post")