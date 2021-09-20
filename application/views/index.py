from flask import render_template, Blueprint
from application import app

bp = Blueprint('index', __name__)

@bp.get('/')
def index():
    return render_template('index.html', title='Title')

app.register_blueprint(bp)
