from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt();
db = SQLAlchemy();

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

class User(db.Model):
    __tablename__ = "users"

    @classmethod
    def register(cls, username, password, email):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        new_user = cls(username=username, password=hashed_utf8, email=email, admin = False)
        db.session.add(new_user)
        return new_user
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(cls.username == username).first()

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    username = db.Column(db.String,
                         primary_key=True,
                         nullable=False,
                         unique=True)
    
    password = db.Column(db.String,
                         nullable=False)
    
    email = db.Column(db.String,
                      nullable=False)
    
    admin = db.Column(db.Boolean,
                      nullable=False)

class Podcast(db.Model):
    __tablename__ = "podcasts"

    @classmethod
    def add_podcast(cls, host, title, description, img_url, podcast_id_spotify):
        new_podcast = cls(host=host, title=title, description=description, img_url=img_url, 
                          podcast_id_spotify=podcast_id_spotify)
        db.session.add(new_podcast)
        return new_podcast

    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True)
    
    host = db.Column(db.String,
                     nullable=False)

    title = db.Column(db.String,
                      nullable=False)
    
    description = db.Column(db.String,
                            nullable=True)
    
    img_url = db.Column(db.String,
                        nullable=True)
    
    podcast_id_spotify = db.Column(db.String,
                           nullable=False)

class WatchList(db.Model):
    __tablename__ = "watch_lists"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    podcast_id = db.Column(db.Integer,
                           db.ForeignKey('podcasts.id'),
                           nullable=False)
    
    user = db.relationship("User",
                           backref="watch_lists")
    
    podcast = db.relationship("Podcast",
                              backref="watch_lists")
    