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
    
    @classmethod
    def make_admin_by_id(cls, id):
        user = cls.get_by_id(id)
        if(user):
            user.admin = True
            db.session.commit()
            return user
        else:
            return None

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

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def delete_podcast(cls, id):
        delete_podcast = cls.get_by_id(id)
        return db.session.delete(delete_podcast)

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

    watchlist = db.relationship("WatchList", cascade="all,delete", backref="podcasts")

class WatchList(db.Model):
    __tablename__ = "watch_lists"

    @classmethod
    def add_item(cls, user_id, podcast_id):
        new_item = cls(user_id=user_id, podcast_id=podcast_id)
        db.session.add(new_item)
        return new_item
    
    @classmethod
    def get_watchlist(cls, user_id):
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def remove_item(cls, user_id, podcast_id):
        delete_item = cls.query.filter(cls.user_id == user_id and cls.podcast_id == podcast_id).first()
        return db.session.delete(delete_item)    

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    podcast_id = db.Column(db.Integer,
                           db.ForeignKey('podcasts.id'),
                           nullable=False)
    
    user = db.relationship("User",
                           backref="watch_lists")
    