from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sys import exc_info
from environs import Env

env = Env()
env.read_env()

print(env.str('DEV_SQLALCHEMY_DATABASE_URI'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = env.str('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey(
        'todolists.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, default=1)

    def __repr__(self):
        return f'<Todos {self.id, self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list',
                            lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<TodoList {self.name, self.todos}>'


@app.route('/')
def index():
    return redirect(url_for('get_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_todos(list_id):
    return render_template('index.html',
                           list=Todo.query.filter_by(
                               todo_list_id=list_id).order_by('id').all(),
                           lists=TodoList.query.order_by('id').all(),
                           listId=list_id
                           )

# Create todo
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    todo_desc = request.get_json()['description']

    try:
        new_todo = Todo(description=todo_desc)
        db.session.add(new_todo)
        db.session.commit()
        body = {
            'description': new_todo.description
        }

    except:
        error = True
        print(exc_info())
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        abort(500)

    else:
        return jsonify(body)


@app.route('/todos/<todo_id>/update', methods=['POST'])
def update_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()

    except:
        print(exc_info())
        db.session.rollback()

    finally:
        db.session.close()

    return redirect('/')


@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        # todo = Todo.query.get(todo_id)
        # db.session.delete(todo)
        todo = Todo.query.filter_by(id=todo_id).delete()
        print(todo)
        db.session.commit()

    except:
        print(exc_info())
        db.session.rollback()

    finally:
        db.session.close()

    return jsonify({'success': True})

# Delete Lists
@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    try:
        todo_list = TodoList.query.get(list_id)
        db.session.delete(todo_list)
        print(todo_list)
        db.session.commit()

    except:
        print(exc_info())
        db.session.rollback()

    finally:
        db.session.close()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
