# from app import app, db, bcrypt  # Ensure bcrypt is initialized in your __init__.py
# from flask import render_template, url_for, flash, redirect
# from app.forms import RegistrationForm, LoginForm
# from app.models import User, Post
# from flask_login import login_user, current_user  # Make sure to import current_user
# from flask import request

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user
from app import db, bcrypt, app
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))  # Redirect to the login page after registration
    return render_template('register.html', title='Register', form=form)
from flask_login import login_user, current_user, logout_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # Redirect to the next page if it exists
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()  # Assuming you have a Post model and want to show all posts
    return render_template('home.html', posts=posts)

