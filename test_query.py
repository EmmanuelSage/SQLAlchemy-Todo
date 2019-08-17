from sqlalchemy.orm import sessionmaker

from database_setup import Todo, Base, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# create Todo

first_todo = Todo(title='Buy milk')

session.add(first_todo)

session.commit()

# Read

session.query(Todo).all()
session.query(Todo).first()

# update Todo

edited_todo = session.query(Todo).filter_by(id=1).one()
edited_todo.description = 'enter the store to buy milk'
session.add(edited_todo)
session.commit()

# Delete Todo

todo_to_delete = session.query(Todo).filter_by(id=1).one()
session.delete(todo_to_delete)
session.commit()