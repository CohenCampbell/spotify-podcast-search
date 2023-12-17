from flask import Flask, render_template, redirect, request, flash, session
#from models import db, connect_db
from forms import RegisterFrom, LoginFrom
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "SUN"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spotify_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

#connect_db(app)
bcrypt = Bcrypt()

@app.route("/create_db")
def db_creation():
    #db.create_all()
    return redirect("/")

@app.route("/")
def homepage():
    if("user" != "loggedin"):
        return redirect("/register")
    
    return render_template("/homepage.html")

@app.route("/register", methods=["GET"])
def get_register():
    form = RegisterFrom()
    return render_template("register.html", form=form)

@app.route("/register", methods=["POST"])
def post_register():
    return redirect("/")

@app.route("/login", methods=["GET"])
def get_login():
    form = LoginFrom()
    return render_template("login.html", form=form)
