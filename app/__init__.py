from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_cors import CORS

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()  # Add Flask-Migrate
bcrypt = Bcrypt()
mongo = PyMongo()
login_manager = LoginManager()


def create_app():
    """Application Factory Pattern to create and configure the Flask application."""
    application = Flask(__name__)
    CORS(application)

    # Set configuration values
    application.config['SECRET_KEY'] = 'your_secret_key_here'
    application.config['DEBUG'] = True
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@localhost/blogdb'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['MONGO_URI'] = "mongodb://localhost:27017/blogdb_nosql"

    # Initialize extensions with the application
    db.init_app(application)
    migrate.init_app(application, db)  # Add migration initialization
    bcrypt.init_app(application)
    mongo.init_app(application)
    login_manager.init_app(application)
    login_manager.login_view = 'routes.login'  # Updated to use blueprint naming

    # Import and register blueprints
    from app.routes import routes_blueprint
    application.register_blueprint(routes_blueprint)

    return application
