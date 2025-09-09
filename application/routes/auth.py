from flask import flash, render_template, request, redirect, url_for, Blueprint
import flask_login
from application import db
from application.models import User
from application.util import hashpw
from application.forms import LoginForm, SignupForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signout', methods=['GET'])
def signout():
    flask_login.logout_user()
    return redirect(url_for('index.index'))

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    login_form = LoginForm()
    if request.method.lower() == 'get':
        return render_template('signin.jinja2', title='Sign In', lf=login_form)
    if login_form.validate_on_submit():
        res = User.query.filter_by(
            email=login_form.email.data,
            password=hashpw(login_form.password.data)
        ).all()
        if len(res) != 0:
            res[0].signin(login_form.remember_me)
        return redirect(url_for('index.index'))
    else:
        flash("Signin Error")
    return redirect(url_for('auth.signin'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method.lower() == 'get':
        return render_template('signup.jinja2', title='Sign Up', sf=signup_form)
    if signup_form.validate_on_submit():
        user = User(
            signup_form.name.data,
            signup_form.email.data,
            signup_form.password.data
        )
        db.session.add(user)
        user.signin(signup_form.remember_me)
        db.session.commit()
        return redirect(url_for('index.index'))
    else:
        flash("Signup Error")
    return redirect(url_for('auth.signup'))
