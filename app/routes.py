# from app import app, db, bcrypt  # Ensure bcrypt is initialized in your __init__.py
# from flask import render_template, url_for, flash, redirect
# from app.forms import RegistrationForm, LoginForm
# from app.models import User, Post
# from flask_login import login_user, current_user  # Make sure to import current_user
# from flask import request
import logging
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user
from app import db, bcrypt, app
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm
from datetime import datetime
from app import mongo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.debug("User already authenticated. Redirecting to home.")
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    logger.debug("Rendering registration form.")
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("Entering login route.")
    if current_user.is_authenticated:
        logger.debug("User already authenticated. Redirecting to home.")
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        logger.debug("Form submitted successfully.")
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            logger.debug(f"User found: {user.id}")
        else:
            logger.debug("User not found.")

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            logger.debug("Password matched. Logging in user.")
            login_user(user, remember=form.remember.data)

            # Log the action in MongoDB
            try:
                logger.debug("Attempting to log action in MongoDB.")
                mongo.db.activity_logs.insert_one({
                    "user_id": user.id,
                    "action": "logged in",
                    "timestamp": datetime.utcnow()
                })
                logger.debug("Action logged successfully in MongoDB.")
            except Exception as e:
                logger.error(f"Error inserting log into MongoDB: {e}")

            next_page = request.args.get('next')
            logger.debug(
                f"Redirecting to: {next_page if next_page else 'home'}")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            logger.warning("Login unsuccessful: Invalid credentials.")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    logger.debug("Rendering login form.")
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logger.debug("Logging out user.")
    logout_user()
    return redirect(url_for('home'))


@app.route("/")
@app.route("/home")
def home():
    logger.debug("Rendering home page.")
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/test-mongo')
def test_mongo():
    try:
        logger.debug("Attempting to insert test document into MongoDB.")
        mongo.db.test.insert_one({"key": "value"})
        logger.debug("Test document inserted successfully.")
        return "MongoDB connected successfully and test document inserted!"
    except Exception as e:
        logger.error(f"Error testing MongoDB connection: {e}")
        return f"Error: {e}"
