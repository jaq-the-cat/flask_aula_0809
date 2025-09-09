from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
from .models import *

with app.app_context() as ctx:
    db.create_all()
    db.session.commit()

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(uid: str):
    return User.query.get(uid)

# Register views
from application.routes.index import bp as index
app.register_blueprint(index)

from application.routes.auth import bp as auth
app.register_blueprint(auth)

from application.routes.tarefas import bp as tarefas
app.register_blueprint(tarefas)
