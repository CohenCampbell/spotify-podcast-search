from flask import Flask, render_template, redirect, request, flash, session
from requests import post, get
from models import db, connect_db, User, Podcast, WatchList
from forms import RegisterFrom, LoginFrom, SpotifyPodcastSearchForm, SpotifyPodcastInfoForm
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os, base64, json

app = Flask(__name__)
app.secret_key = "SUN"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spotify_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
bcrypt = Bcrypt()
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:5000/"


def get_spofigy_token(code):
    
    auth_string = client_id + ":" + client_secret
    auth_string64 = base64.b64encode(auth_string.encode()).decode()
    url = "https://accounts.spotify.com/api/token"

    headers = {
        'Authorization': "Basic " + auth_string64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials',
            'code': code,
            'redirect_uri': redirect_uri}
    
    result = post(url, headers=headers, data=data)
    
    token = json.loads(result.content)
    return token["access_token"]



@app.route("/create_db")
def db_creation():

    db.create_all()
    return redirect("/")

@app.route("/")
def homepage():

    if "user_id" not in session:
        flash("You must be logged in to view that page!")
        return redirect("/login")

    #check if the user accepts the request, if not flashes an error
    if "error" in request.args:
        flash("You must accept the request or the application cannot function")
        return redirect("/login")

    # getting spotify code, needed for spotify token, assigned None if it's not in query str
    if request.args:
        code = request.args["code"]
    else:
    # Gets code if it wasn't in query str
        return redirect(f"https://accounts.spotify.com/en/authorize?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}")
    
    user = User.get_by_id(session["user_id"])

    return render_template("/homepage.html", code=code or None, admin=user.admin)

@app.route("/register", methods=["GET"])
def get_register():

    form = RegisterFrom()
    return render_template("register.html", form=form)

@app.route("/register", methods=["POST"])
def post_register():

    form = RegisterFrom()
    if(form.validate_on_submit()):
        username = form.username.data
        password = form.password.data
        email = form.email.data
        
        new_user = User.register(username, password, email)
        db.session.commit()

        session["user_id"] = new_user.id
        session["admin"] = new_user.admin
        return redirect("/")
    flash("There was an error!")
    return redirect("/register")

@app.route("/login", methods=["GET"])
def get_login():

    form = LoginFrom()
    return render_template("login.html", form=form)

@app.route("/login", methods=["POST"])
def post_login():

    form = LoginFrom()
    username = form.username.data
    password = form.password.data

    logged_user = User.get_by_username(username)
    if(logged_user == None):
        flash("Incorrect username or password")
        return redirect("/login")
    
    session["user_id"] = logged_user.id
    session["admin"] = logged_user.admin
    return redirect("/")
    

@app.route("/logout", methods=["GET"])
def logout():

    session.clear()
    flash("You have logged out!")
    return redirect("/login")

@app.route("/podcastAPI", methods=["POST"])
def podcast_post():

    form = SpotifyPodcastSearchForm()

    if(form.validate_on_submit()):
        query = form.search.data.replace(" ", "+")
        code = form.code.data
    else:
        flash("There was an error with your search. Please try again!")
        return redirect("/podcast")

    url = f"https://api.spotify.com/v1/shows/{query}"                           #f'https://api.spotify.com/v1/search?q={query}&type=show&limit=5'
    token = get_spofigy_token(code)
    headers = {'Authorization': 'Bearer ' + token}
    
    results = get(url, headers=headers)
    results_json = json.loads(results.content)
    
    
    if results.json:
        if "error" in results_json:
            flash("invalid id")
            return redirect("/podcastAPI")

        show = dict(name = results_json["name"], 
                description = results_json["description"], 
                host = results_json["publisher"], 
                image_url = results_json["images"][0]["url"],
                podcast_id = results_json["id"])
        
        return render_template("/podcastAPI.html", form=form, podcast=show, data_form=SpotifyPodcastInfoForm())

    return redirect("/podcast")

@app.route("/podcastAPI", methods=["Get"])
def podcast_get():
    
    if "user_id" not in session:
        flash("You must be logged in to view that page!")
        return redirect("/login")
    elif session["admin"] != True:
        flash("You must be an admin to view that page!")
        return redirect("/")

    form = SpotifyPodcastSearchForm()
    
    return render_template("/podcastAPI.html", form=form)

@app.route("/podcast", methods=["GET"])
def show_podcast_db():

    if "user_id" not in session:
        flash("You must be logged in to view that page!")
        return redirect("/login")
    
    podcasts = Podcast.query.all();

    return render_template("/podcast.html", podcasts=podcasts)

@app.route("/podcast", methods=["POST"])
def podcast_add_db():
    
    form = SpotifyPodcastInfoForm()
    if(form.validate_on_submit()):
        new_podcast = Podcast.add_podcast(host=form.host.data, title=form.title.data, 
                                          description=form.description.data, img_url=form.img_url.data, 
                                          podcast_id_spotify=form.podcast_id_spotify.data)
        db.session.commit()
        flash(f"{form.title.data} was added to the database!")
        return redirect("/podcastAPI")
    return redirect("/podcastAPI")
    
    