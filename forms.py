from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Length, InputRequired

class RegisterFrom(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20, min=1)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=1)])
                             
    email = EmailField("Email", validators=[InputRequired(), Length(min=1)])

class LoginFrom(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20, min=1)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=1)])