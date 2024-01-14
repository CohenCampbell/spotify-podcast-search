from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, HiddenField
from wtforms.validators import Length, InputRequired

class RegisterFrom(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20, min=1)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=1)])
                             
    email = EmailField("Email", validators=[InputRequired(), Length(min=1)])

class LoginFrom(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20, min=1)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=1)])

class SpotifyPodcastSearchForm(FlaskForm):
    search = StringField("Search", validators=[Length(min=1)])

class SpotifyPodcastInfoForm(FlaskForm):
    host= HiddenField("host")
    title= HiddenField("title")
    description = HiddenField("description")
    img_url= HiddenField("img_url")
    podcast_id_spotify= HiddenField("podcast_id_spotify")