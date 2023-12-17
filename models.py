from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt();
db = SQLAlchemy();

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

