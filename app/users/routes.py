import secrets, os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import app, db, bcrypt
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.quotes.forms import QuoteForm
from app.models import User, Quote, UserProfile
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        username=current_user.username
        return redirect((url_for('users.user_home', username=current_user.username)))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('users.user_home', username=current_user.username)))
        #return redirect((url_for('main.home')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect((url_for('users.user_home', username=current_user.username)))
            #return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user_profile = UserProfile(
            authors=current_user, #changed authors to author, recreate database after changing relationships and keys in models.py
            full_name=form.full_name.data,
            address_one=form.address_one.data,
            address_two=form.address_two.data,
            city=form.city.data,
            state=form.state.data,
            zipcode=form.zipcode.data
        )
        db.session.add(user_profile)
        db.session.commit()
        flash('Your profile has been saved', 'success')
        return redirect(url_for('main.home'))
    # elif request.method == 'GET':
    #     form.username.data = current_user.username
    #     form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@users.route('/userhome/<string:username>')
@login_required
def user_home(username):
    if current_user.username == username:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        quotes = Quote.query.filter_by(author=user).paginate(page=page, per_page=2)
        return render_template('user_home.html', quotes=quotes, user=user)
    else:
        return render_template('403.html'), 403
