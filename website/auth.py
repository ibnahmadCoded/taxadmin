from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
#from . import db
from .forms import LoginForm #, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.index'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_superuser:
        flash('Only superusers can register new users.')
        return redirect(url_for('admin.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_superuser=form.is_superuser.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user has been created!')
        return redirect(url_for('admin.index'))
    return render_template('register.html', form=form)"""