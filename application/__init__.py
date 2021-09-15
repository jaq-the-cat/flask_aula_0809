# type: ignore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from application.widget import Widget
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

from application.models import User
@login_manager.user_loader
def load_user(uid: str):
    return User.query.get(uid)

# Initialize widgets
from application.widgets_ext import Widget
widget = Widget(app)

# Register widgets and views
from application.widgets import *
import application.views.index
import application.views.auth
