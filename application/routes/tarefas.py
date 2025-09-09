from flask import flash, render_template, request, redirect, url_for, Blueprint
import flask_login
from application import db
from application.models import Tarefa, User
from application.forms import TarefaForm

bp = Blueprint('tarefas', __name__, url_prefix='/tarefas')

@bp.route('/', methods=['GET', 'POST'])
@flask_login.login_required
def index():
    tarefa_form = TarefaForm()
    if request.method.lower() != 'get':
        if tarefa_form.validate_on_submit():
            tarefa = Tarefa(tarefa_form.description.data, flask_login.current_user.uid)
            db.session.add(tarefa)
            db.session.commit()
        else:
            flash("Create Error")
    # tarefas = Tarefa.query.filter_by(user_id=flask_login.current_user.uid)
    tarefas = Tarefa.query.all()
    return render_template('tarefas.jinja2', title='Tarefas', tf=tarefa_form, tarefas=tarefas)

@bp.route('/update/<uid>', methods=['GET', 'POST'])
@flask_login.login_required
def update(uid: str):
    tarefa: Tarefa = Tarefa.query.get(uid)
    tarefa_form = TarefaForm()

    if request.method.lower() != 'get':
        if tarefa_form.validate_on_submit():
            tarefa.description = tarefa_form.description.data
            db.session.commit()
        else:
            flash("Update Error")

    tarefa_form.description.data = tarefa.description
    return render_template('tarefaUpdate.jinja2', title='Tarefa Update',
        tarefa=tarefa, tf=tarefa_form)


@bp.route('/delete/<uid>', methods=['POST'])
@flask_login.login_required
def delete(uid: str):
    tarefa: Tarefa = Tarefa.query.get(uid)
    if tarefa.user_id == flask_login.current_user.uid:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect(url_for('tarefas.index'))