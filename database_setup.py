import sys

from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    is_completed = Column(Boolean, default=False)

engine = create_engine('sqlite:///todo.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)