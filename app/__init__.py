
# from application import routes
# from application.routes import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your_secret_key_here'
application.config['DEBUG'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@localhost/blogdb'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['MONGO_URI'] = "mongodb://localhost:27017/blogdb_nosql"


mongo = PyMongo(application)
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'


# Inline import to avoid circular imports
def register_routes():
    from application import routes


register_routes()
