from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sys import exc_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skywalker:password@localhost:5432/flask_todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todos {self.id, self.title, self.description}>'


todo1 = Todo(title='foo', description='Make foo')
todo2 = Todo(title='bar', description='Make bar')
todo3 = Todo(title='fooz', description='Make fooz')
todo4 = Todo(title='barz', description='Make barz')


db.create_all()

# db.session.add_all([todo1, todo2, todo3, todo4])

# db.session.commit()


@app.route('/')
def todos():
    return render_template('index.html', data=Todo.query.all())


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = None
    todo_name = request.get_json()['todo']
    todo_desc = request.get_json()['description']
    print(todo_name)

    try:
        new_todo = Todo(title=todo_name, description2=todo_desc)
        db.session.add(new_todo)
        db.session.commit()
        body = {
            'todo': new_todo.title,
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


if __name__ == '__main__':
    app.run()
