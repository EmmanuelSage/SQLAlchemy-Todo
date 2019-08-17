from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Todo, engine

# create database session
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the todos in our database
# This function operate on the Read operation.
@app.route('/')
@app.route('/todos')
def show_todos():
    todos = session.query(Todo).all()
    return render_template("todos.html", todos=todos)


# This will let us Create a new todo and save it in our database
@app.route('/new/todo', methods=['GET', 'POST'])
def new_todo():
    if request.method == 'POST':
        newTodo = Todo(title=request.form['title'], description=request.form['description'])
        session.add(newTodo)
        session.commit()
        return redirect(url_for('show_todos'))
    else:
        return render_template('newTodo.html')


# This will let us Update our todo name and save it in our database
@app.route("/todos/<int:todo_id>/edit/", methods=['GET', 'POST'])
def edit_todo(todo_id):
    edited_todo = session.query(Todo).filter_by(id=todo_id).one()
    if request.method == 'POST':
        if request.form['title']:
            edited_todo.title = request.form['title']
            return redirect(url_for('show_todos'))
    else:
        return render_template('editTodo.html', todo=edited_todo)


# This will let us Delete our todo
@app.route('/todos/<int:todo_id>/delete/', methods=['GET', 'POST'])
def delete_todo(todo_id):
    todo_to_delete = session.query(Todo).filter_by(id=todo_id).one()
    if request.method == 'POST':
        session.delete(todo_to_delete)
        session.commit()
        return redirect(url_for('show_todos', todo_id=todo_id))
    else:
        return render_template('deleteTodo.html', todo=todo_to_delete)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4003)