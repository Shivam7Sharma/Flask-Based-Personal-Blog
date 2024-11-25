import logging
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user
from app import db, bcrypt, mongo
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a blueprint
routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.debug("User already authenticated. Redirecting to home.")
        return redirect(url_for('routes.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.debug(f"New user registered: {user.username}")
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    logger.debug("Rendering registration form.")
    return render_template('register.html', title='Register', form=form)

# werkzeug.routing.BuildError: Could not build url for endpoint 'login'. Did you mean 'routes.login' instead?


@routes_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("Entering login route.")
    if current_user.is_authenticated:
        logger.debug("User already authenticated. Redirecting to home.")
        return redirect(url_for('routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        logger.debug("Form submitted successfully.")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            logger.debug("Password matched. Logging in user.")
            login_user(user, remember=form.remember.data)
            # Log the action in MongoDB
            try:
                mongo.db.activity_logs.insert_one({
                    "user_id": user.id,
                    "action": "logged in",
                    "timestamp": datetime.utcnow()
                })
            except Exception as e:
                logger.error(f"Error inserting log into MongoDB: {e}")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.home'))
        else:
            logger.warning("Login unsuccessful: Invalid credentials.")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    logger.debug("Rendering login form.")
    return render_template('login.html', title='Login', form=form)


@routes_blueprint.route("/logout")
def logout():
    logger.debug("Logging out user.")
    logout_user()
    return redirect(url_for('routes.home'))


@routes_blueprint.route("/")
@routes_blueprint.route("/home")
def home():
    logger.debug("Rendering home page.")
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@routes_blueprint.route('/test-mongo')
def test_mongo():
    try:
        logger.debug("Attempting to insert test document into MongoDB.")
        mongo.db.test.insert_one({"key": "value"})
        logger.debug("Test document inserted successfully.")
        return "MongoDB connected successfully and test document inserted!"
    except Exception as e:
        logger.error(f"Error testing MongoDB connection: {e}")
        return f"Error: {e}"
