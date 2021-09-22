from application import db
from application.util import hashpw
from flask_login import login_user, logout_user
from uuid import uuid4

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    suspended = db.Column(db.Boolean, nullable=False)

    def __init__(self, name: str, email: str, password: str):
        self.uid = str(uuid4())
        self.name = name
        self.email = email
        self.password = hashpw(password)
        self.suspended = False

    def signin(self, rember: bool):
        login_user(self, remember=rember)

    def __repr__(self):
        return f'User<{self.email} : {self.name}>'

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return not self.suspended

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.uid
