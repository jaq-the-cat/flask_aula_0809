# type: ignore
from flask import render_template, request, redirect, url_for, Blueprint
from application import app, db
from application.models import User
from application.util import hashpw

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/')
def auth():
    return render_template('auth.html', title='Auth')

@bp.post('/login')
def login():
    res = User.query.filter_by(
        email=request.form['email'],
        password=hashpw(request.form['password'])
    ).all()
    if len(res) != 0:
        res[0].login(request.form['rember'])
    return redirect(url_for('index.index'))

@bp.post('/signup')
def signup():
    db.session.add(User(
        request.form['name'],
        request.form['email'],
        request.form['password']))
    db.session.commit()
    return redirect(url_for('index.index'))

app.register_blueprint(bp)
