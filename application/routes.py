# type: ignore
from flask import render_template, request, redirect, url_for
from application import app, db
from application.models import User
from application.util import hashpw

@app.get('/')
def index():
    return render_template('index.html', title='Title')

@app.get('/auth')
def auth():
    return render_template('auth.html', title='Auth')

@app.post('/login')
def login():
    res = User.query.filter_by(
        email=request.form['email'],
        password=hashpw(request.form['password'])
    ).all()
    if len(res) != 0:
        res[0].login(request.form['rember'])
    return redirect(url_for('index'))

@app.post('/signup')
def signup():
    db.session.add(User(
        request.form['name'],
        request.form['email'],
        request.form['password']))
    db.session.commit()
    return redirect(url_for('index'))
