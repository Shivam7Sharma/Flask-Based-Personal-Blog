from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

# Initialize extensions globally
db = SQLAlchemy()
bcrypt = Bcrypt()
mongo = PyMongo()
login_manager = LoginManager()


def create_app():
    """Application Factory Pattern to create and configure the Flask app."""
    application = app = Flask(__name__)

    # Set configuration values
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@localhost/blogdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = "mongodb://localhost:27017/blogdb_nosql"

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'  # Updated to use blueprint naming

    # Import and register blueprints
    from application.routes import routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
