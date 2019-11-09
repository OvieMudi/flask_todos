from flask import Flask, render_template, request, jsonify, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sys import exc_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skywalker:password@localhost:5432/flask_todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todos {self.id, self.description}>'


# todo1 = Todo( description='Make foo')
# todo2 = Todo( description='Make bar')
# todo3 = Todo( description='Make fooz')
# todo4 = Todo( description='Make barz')


# db.create_all()

# db.session.add_all([todo1, todo2, todo3, todo4])

# db.session.commit()


@app.route('/')
def index():
    return redirect('/todos')


@app.route('/todos')
def todos():
    return render_template('index.html', data=Todo.query.order_by('id').all())


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


if __name__ == '__main__':
    app.run()
