from app import db, Todo, TodoList

list = TodoList(name='urgent')

todo1 = Todo(description='Do something awesome')
todo2 = Todo(description='Do something crazy')
todo3 = Todo(description='Play PES20')

todo1.list = list
todo2.list = list
todo3.list = list

db.session.add(list)
db.session.commit()
