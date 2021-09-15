# type: ignore
from flask import render_template, request, redirect, url_for, Blueprint
from application import app, db
from application.models import User
from application.util import hashpw
from application.forms import LoginForm, SignupForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/')
def auth():
    login_form = LoginForm()
    signup_form = SignupForm()
    return render_template('auth.html', title='Auth',
        login_form=login_form, signup_form=signup_form)

@bp.post('/login')
def signin():
    login_form = LoginForm()
    if login_form.validate_on_submit:
        res = User.query.filter_by(
            email=login_form.email,
            password=hashpw(login_form.password)
        ).all()
        if len(res) != 0:
            res[0].signin(login_form.remember_me)
        return redirect(url_for('index.index'))
    return redirect(url_for('auth.auth'))

@bp.post('/signup')
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        db.session.add(User(
            signup_form.name,
            signup_form.email,
            signup_form.password
        ))
        db.session.commit()
        return redirect(url_for('index.index'))
    return redirect(url_for('auth.auth'))

app.register_blueprint(bp)
