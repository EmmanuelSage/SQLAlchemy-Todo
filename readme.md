# Sql Alchemy

This is a project to learn SQLAlchemy

## Implementation with raw queries

> We could write raw queries with pythons inbuilt sqlite3 connection

- create a rawquery.py file and add

```py {.line-number}
import sqlite3

#connects it to the rawquery db and creates it if it does not exist
# conn = sqlite3.connect('rawquery.db', check_same_thread=False) to supress same thread error
conn = sqlite3.connect('rawquery.db')


#creates the cursor
cur = conn.cursor()

#execute the query which creates the todo called test with id and name
#as the columns
cur.execute('''
    CREATE TABLE todo
    (id INTEGER PRIMARY KEY ASC,
     name varchar(250) NOT NULL)
''')

#executes the query which inserts values in the table
cur.execute("INSERT INTO test VALUES(1, 'The first todo is inputed into the database')")

#commits the executions
conn.commit()

#closes the connection
conn.close()
```

- we import the native sqlite3
- we create a connection to a database 'rawquery.db', this creates the db file if it doesn't exist
- we create a cursor that would write to the file
- we execute the queries with the cursor object
- we use the conn object to commit and close the db connection

> run `$ python rawquery.py`
- This would run the file create the .db file and run the queries


## Implementation with SQLAlchemy

> run `$ pip install sqlalchemy` to install sqlalchemy

> Lets create a database_setup.py file to setup our database add this to the file

```py {.line-numbers}
import sys

from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///todo.db')

Base.metadata.create_all(engine)
```

- we import stuff for database table config from sqlalchemy
- we import declarative_base to define a base class that all our model class would inherit
- we use create engine to define our database
- we use `Base.metadata.create_all(engine)` to add the classes we write

> add this to the database_setup.py right after the Base declaration

```py
......./

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    is_completed = Column(Boolean, default=False)

engine = create_engine('sqlite:///todo.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
```

- We create a Todo class that will define our table
- we set the table name with the internal variable \__tablename\__
- we then define the columns
- setting primary_key to True means we want to make this column a primary key
- Integer, String(250) and Boolean are datatypes
- nullable means the column must be filled for the row to be created
- default sets a default value for the column if none is provided
- `connect_args={'check_same_thread': False}` is to supress same thread error sqlalchemy throws when the connection object is not set in the method that uses it.

> we can run `$ python database_setup.py` to create our database with the table

> create a test_query.py file

```py
from sqlalchemy.orm import sessionmaker

from database_setup import Todo, Base, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


```
- we import our setup from the database_setup file
- we then use `Base.metadata.bind = engine` to make connections betweeen our tables and our class definitions
- we setup a session object for making the crud operations

> To create a Todo the general pattern would be the below
```py
entryName = ClassName(property='value', property='value')
# or better explained
entryName = tableOrModelName(column='value', column='value')

# to add our entry to our current session
session.add(entryName)

# to commit the transaction to our database
session.commit()
```
- Hence to create a todo we would add this to the test_query.py file

```py
# create Todo

first_todo = Todo(title='Buy milk')

session.add(first_todo)

session.commit()
```
> To Get or Read a Todo

- We could use `session.query(Todo).all()` to return all Todo as a list of Todo objects
- We could use `session.query(Todo).first()` to return the first result or `None` if it doesn't exist
- We could also use `.one()` to return one result or raise an `sqlalchemy.orm.exc.NoResultFound` exception if no result is found or multiple results are found

- add this to the file
```py
# Read

session.query(Todo).all()
session.query(Todo).first()

```

> to update a todo

- to update a todo we need to
    - find the entry
    - change the values
    - add the new entry
    - commit the session to the database

- add this to the code
```py
# update Todo

edited_todo = session.query(Todo).filter_by(id=1).one()
edited_todo.description = 'enter the store to buy milk'
session.add(edited_tod0)
session.commit()

```

- the above would add a description to our todo

> To Delete a Todo

- to delete we do the following
    - find the entry
    - delete the entry
    - commit the session

- add the following code to delete the todo

```py
# Delete Todo

todo_to_delete = session.query(Todo).filter_by(id=1).one()
session.delete(todo_to_delete)
session.commit()

```

> run `$ python test_query.py` and check the database to see that it has been added

- Because we made the description field nullable we do not need to provide it, when we create
- is_completed would be set to '0' which means false as this is the default

> This concludes our SQLAlchemy tutorial, but to interact with it, we could create a Flask server.

>Run `$ pip install flask`
> Add the code below to an app.py file

```py
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

```

> Create a templates folder and add
    - deleteTodo.html
    - editTodo.html
    - newTodo.html
    - todos.html

> add this code to deleteTodo.html
```py
<h2> Are you sure you want to delete todo: {{todo.title}}? </h2>
<form action="#" method='post'>
    <button type="submit"> Delete</button>
    <a href='{{url_for('show_todos')}}'>
    <button> Cancel</button>
    </a>
</form>

```

> add this code to editTodo.html
```py
<form action="{{ url_for('edit_todo',todo_id = todo.id)}}" method="post">
        <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" class="form-control" name="title" value="{{todo.title }}">
            <button type="submit"> SAVE</button>
            <a href='{{url_for('show_todos')}}'>
                <button>Cancel</button>
            </a>
        </div>
    </form>

```

> add this code to newTodo.html
```py
<h1>Add a Todo</h1>
<form action="#" method="post">
   <div class="form-group">
       <label for="name">Title:</label>
       <input type="text" maxlength="100" name="title" placeholder="Title of the todo">

       <label for="author">Description:</label>
       <input maxlength="100" name="description" placeholder="description of the todo">

       <button type="submit">Create</button>
   </div>
</form>

```

> add this code to todos.html
```py
<html>
  <body>
    <h1>Todos</h1>
    <a href="{{ url_for('new_todo') }}">
      <button>Add Todo</button>
    </a>
    <ul>
      {% for todo in todos %}
      <li>Title : {{ todo.title }}</li>
      <li>Description : {{ todo.description }}</li>

      <a href="{{url_for('edit_todo', todo_id = todo.id )}}">
        Edit
      </a>
      <a
        href="{{url_for('delete_todo', todo_id = todo.id )}}"
        style="margin-left: 10px;"
      >
        Delete
      </a>
      <br />
      <br />
      {% endfor %}
    </ul>
  </body>
</html>

```

> run `$ python app.py` to start the application and check your browser

### Todo
- explain flask setup
- improve ui with css
- implement is_completed in ui