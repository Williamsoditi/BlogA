from flask import render_template, redirect, url_for, request, flash
from ..models import User
from . import auth
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user
from .forms import SignupForm, LoginForm
from ..email import mail_message

@auth.route('/signup', methods = ["GET","POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.name.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Blog-A", "email/welcome_user", user.email, user = user)

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/signup.html' , signup_form = form)
    
@auth.route('/login', methods = ["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash("Invalid username or password")

    title = "Blog-A Login"
    return render_template('auth/login.html', login_form = login_form, title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))