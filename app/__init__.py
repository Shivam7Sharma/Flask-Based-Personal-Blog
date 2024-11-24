
# from app import routes
# from app.routes import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@localhost/blogdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MONGO_URI'] = "mongodb://localhost:27017/blogdb_nosql"


mongo = PyMongo(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Inline import to avoid circular imports
def register_routes():
    from app import routes


register_routes()
